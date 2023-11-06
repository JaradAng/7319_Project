import psycopg2
from PIL import ImageFont, Image, ImageDraw
import hyperlpr3 as lpr3
import cv2
import random
import string
import numpy as np

class VehicleSecurityAnalysis:
    def __init__(self, db_config):
        # self.conn = psycopg2.connect(**db_config)
        self.catcher = lpr3.LicensePlateCatcher(detect_level=lpr3.DETECT_LEVEL_HIGH)
        self.font_ch = ImageFont.truetype("EventConsumer/platech.ttf", 20, 0)  # Replace with the path to your font file
        pass

    def draw_plate_on_image(self, img, box, text):
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (x1, y1), (x2, y2), (139, 139, 102), 2, cv2.LINE_AA)
        cv2.rectangle(img, (x1, y1 - 20), (x2, y1), (139, 139, 102), -1)
        data = Image.fromarray(img)
        draw = ImageDraw.Draw(data)
        draw.text((x1 + 5, y1 - 20), text, (255, 255, 255), font=self.font_ch)
        res = np.asarray(data)
        return res
    
    def license_plate_reader(self):
        letters = ''.join(random.choice(string.ascii_uppercase) for i in range(3))
        numbers = ''.join(random.choice(string.digits) for i in range(4))
        return f"{letters} {numbers}"

    def analyze(self, track):
       
       print("Performing security analysis for vehicles...")
        
       box = track[:4]
       frame = track[-1]  # Replace with the actual frame data if different
       results = self.catcher(frame)
       for code, confidence, type_idx, plate_box in results:
           text = f"{code} - {confidence:.2f}"
           frame = self.draw_plate_on_image(frame, plate_box, text)
        
        
       
       license_plate = self.license_plate_reader()
       time_of_day = track.get('time_of_day', 'day') 
       dwelling_time = track.get('dwelling_time', 0)  # Time in seconds
        
       safe_license_plates = ["XYZ 123", "ABC 789"]  # Dummy  plates so model does not break
       if license_plate not in safe_license_plates:
            print("Unknown vehicle detected.")
        
       if time_of_day == 'night' and dwelling_time > 600:
            print("Suspicious vehicle detected: Long dwelling time during night.")

        # cursor = self.conn.cursor()
        # cursor.execute(
        #     "INSERT INTO vehicle_analysis (license_plate, vehicle_count) VALUES (%s, %s)",
        #     (license_plate, vehicle_count)
        # )
        # self.conn.commit()
        # cursor.close()
