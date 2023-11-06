
import requests
import logging
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class PersonSecurityAnalysis:
    def __init__(self, db_config):
        # self.conn = psycopg2.connect(**db_config)
        self.high_risk_zones = [(0, 200, 200, 400), (300, 300, 400, 400)]  # Replace with actual coordinates
        self.time_in_zone = {}
        pass

    def find_zone(self, bbox):
        x1, y1, x2, y2 = bbox
        for hx1, hy1, hx2, hy2 in self.high_risk_zones:
            if hx1 <= x1 and hy1 <= y1 and hx2 >= x2 and hy2 >= y2:
                return 'high-risk'
        return 'low-risk'
    

    def send_to_frontend(self, data):
        try:
            response = requests.post("http://localhost:8000/add_person_data/", json=data)
            response.raise_for_status()
            print("Data sent to frontend successfully.")
        except requests.RequestException as e:
            print(f"Failed to send data to frontend: {e}")

    def analyze(self, track):
        track = track[:6]
        x1, y1, x2, y2, _, track_id = map(int, track)
        zone = self.find_zone((x1, y1, x2, y2))

        suspicious_activity = False
        if track_id not in self.time_in_zone:
            self.time_in_zone[track_id] = 0
        self.time_in_zone[track_id] += 1

        if zone == 'high-risk' and self.time_in_zone[track_id] > 120:
            print(f"Suspicious activity detected: Person {track_id} lingering in high-risk zone.")
            suspicious_activity = True
        elif zone == 'low-risk' and self.time_in_zone[track_id] <= 120:
            print(f"No risk detected for Person {track_id}.")
        else:
            print(f"Person {track_id} is in a {zone} zone but not lingering.")  # Assuming each frame is ~1s. Otherwise adjust accordingly.


        crowd_density = 1  # Dummy value, calculate based on the number of persons detected
        if crowd_density > 5:
            print("High crowd density detected.")


        data_to_send = {
            "track_id": track_id,
            "zone": zone,
            "suspicious_activity": suspicious_activity,
            # Add more fields as needed
        }

        # Send data to frontend
        self.send_to_frontend(data_to_send)





### Future Improvements
# import psycopg2
# import cv2
# import asyncio
# import aiohttp

#Database Connection

        # cursor = self.conn.cursor()
        # cursor.execute(
        #     "INSERT INTO person_analysis (suspicious_activity, crowd_density) VALUES (%s, %s)",
        #     (suspicious_activity, crowd_density)
        # )
        # self.conn.commit()
        # cursor.close()

#predictive modeling

#         self.predictive_model = self.load_predictive_model()


#     def load_predictive_model(self):
#         # Placeholder: Load your trained predictive model here
#         return RandomForestClassifier()  # Replace with the actual model


#         # Predictive Modeling (assuming features are x1, y1, x2, y2, and crowd_density)
#         features = np.array([x1, y1, x2, y2, crowd_density]).reshape(1, -1)
#         risk_score = self.predictive_model.predict_proba(features)[0][1]

# Async Posting

#     async def send_to_frontend(self, data):
#         async with aiohttp.ClientSession() as session:
#             async with session.post("http://localhost:8000/add_person_data/", json=data) as response:
#                 if response.status == 200:
#                     print("Data sent to frontend successfully.")
#                 else:
#                     print(f"Failed to send data to frontend: {response.status}")