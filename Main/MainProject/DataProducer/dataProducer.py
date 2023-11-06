
import os
import time
import numpy as np
import omegaconf
#import redis
from datetime import datetime
import pickle
from loguru import logger
import cv2
import torch
from ultralytics import YOLO
from boxmot import trackers

from boxmot.tracker_zoo import create_tracker
from boxmot.utils import ROOT, WEIGHTS
from boxmot.utils.checks import TestRequirements
from EventListener.eventListener import EventListener

import os

class DataProducer:
    def __init__(self, config_file='DataProducer/config.yaml', yolo_model='yolov8n.pt', log_file='logs/orchestrator.log'):
        # Initialize Redis
        # self.r = redis.Redis(host='redis-fare', port=6379)
        # self.r.flushall()

        # Initialize Logger
        self.logger = logger
        if os.path.isfile(log_file):
            os.remove(log_file)
        self.logger.add(log_file)

        #Set up Observer
        self.observers = []

        # Load Configurations
        self.cfg = omegaconf.OmegaConf.load(config_file)
        self.bbox_crop = self.cfg[self.cfg.use]
        
        # Initialize YOLO Model
        self.yolo = YOLO(yolo_model)
        
        # Setup Video Capture
        self.capture = cv2.VideoCapture(self.cfg.input_video)
        
        
        # Initialize Frame Number
        self.frame_number = 0

        # Class IDs for vehicles and persons
        self.interested_classes = [0, 2, 3, 8]  # Update this based on your YOLO model

        #tracker
        
        self.tracker = create_tracker(
                'bytetrack',
                tracker_config='DataProducer/boxmot/configs/bytetrack.yaml',
                reid_weights='osnet_x0_25_msmt17.pt',
                device='cpu',
                half=False,
                per_class=False
            )
        
    def register_observer(self, observer):
        """Register an observer that will receive updates."""
        self.observers.append(observer)

    def notify_observers(self, data):
        """Notify all registered observers."""
        for observer in self.observers:
            observer.process_data(data)

    #Save crops to be sent for security analysis

    def save_cropped_objects(self, tracker_output, frame):
        for track in tracker_output:
            if len(track) == 6:
                x1, y1, x2, y2, _, class_id = map(int, track)
                track_id = track[4] 
            elif len(track) == 7:
                x1, y1, x2, y2, _, class_id, track_id = map(int, track)
            else:
                print(f"Unexpected number of values in track: {len(track)}")
                continue
            cropped_image = frame[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            object_type = "person" if class_id == 0 else "vehicle"
            filename = f"{object_type}_{track_id}_{timestamp}.png"

            # Create a directory to save the images if it doesn't exist
            save_path = f"Crops/{object_type}"
            os.makedirs(save_path, exist_ok=True)

            try:
                success = cv2.imwrite(os.path.join(save_path, filename), cropped_image)
                if not success:
                    print(f"Could not save the image at {os.path.join(save_path, filename)}")
            except Exception as e:
                print(f"An error occurred while saving the image: {e}")
        

    def run(self):
        while True:
            start = time.time()
            ret, frame = self.capture.read()

            save_interval = 30
            
            if frame is None:
                self.terminate()
                break

            # Pre-processing
            s1 = time.time()
            frames = []
            for box in self.bbox_crop:
                x1, y1, x2, y2 = box
                cropped_frame = frame[y1:y2, x1:x2]
                frames.append(cropped_frame)

            # YOLO Detection
            s2 = time.time()
            res = self.yolo.track(source=frame, classes=0, conf=0.5122620708221085, persist=True, verbose=False, show=False, device="cpu")
            
            filtered_res = [r for r in res if any(class_id in r.names.keys() for class_id in self.interested_classes)]
            all_boxes = []
            for r in filtered_res:
                # Directly get the bounding boxes and other attributes
                boxes = r.boxes.data  # Should be a numpy array or torch.Tensor
                
                # If 'boxes' is a torch.Tensor, convert it to numpy
                if isinstance(boxes, torch.Tensor):
                    boxes = boxes.cpu().numpy()
                
                
                # Iterate through each box and extract details
                for box in boxes:
                    x1, y1, x2, y2, conf = box[:5]  # Assuming the fifth element is confidence
                    class_id = 0  # Placeholder, adjust as needed
                    
                    all_boxes.append([x1, y1, x2, y2, conf, class_id])


            # Convert to numpy array for tracker
            all_boxes_np = np.array(all_boxes)

            if all_boxes_np.shape[0] == 0:
                print("No detections. Creating an empty 2D array.")
                all_boxes_np = np.empty((0, 6))


            if self.frame_number % save_interval == 0:
                self.save_cropped_objects(all_boxes_np, frame)



            # filtered_res = [r for r in res if any(class_id in r.names.keys() for class_id in self.interested_classes)]
            # filtered_res_np = np.array([[r.x1, r.y1, r.x2, r.y2, r.conf, r.class_id] for r in filtered_res])
            # print(filtered_res)
            tracker = self.tracker.update(all_boxes_np, self.frame_number)

            print(tracker)            

            # Post-processing
            s3 = time.time()
           

            # Redis Operations
            s4 = time.time()
            data_to_store = {
                'frame': frame,
                'tracker_output': tracker,  
                'timestamp': datetime.now(),
                'kill': False,
                'frame_number': self.frame_number
            }
            self.notify_observers(data_to_store)

            end = time.time()
            self.logger.info(f"Frame: {self.frame_number}, FPS: {1 / (end - start)}")
            self.frame_number += 1

    def terminate(self):
        self.logger.info("DataProducer is terminating.")
        # Any additional cleanup can go here

if __name__ == "__main__":
    db_config = {}  # Your database configuration
    listener = EventListener(db_config=db_config)
    
    producer = DataProducer()
    producer.register_observer(listener)
    producer.run()

