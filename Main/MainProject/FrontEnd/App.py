import streamlit as st
import requests
import time
import os
import glob
import pandas as pd
from PIL import Image

def resize_image(image_path, base_width):
        
        img = Image.open(image_path)
        w_percent = base_width / float(img.size[0])
        h_size = int(float(img.size[1]) * float(w_percent))
        img = img.resize((base_width, h_size), Image.LANCZOS)
        
        return img


class StreamlitDashboard:
    def __init__(self):
        if 'unique_track_ids' not in st.session_state:
            st.session_state.unique_track_ids = []
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0

    def initialize_data(self):
        st.session_state.unique_track_ids = sorted(list(set(entry["track_id"] for entry in requests.get("http://localhost:8000/get_person_data/").json().get("data", []))))


    def get_risk_counts(self, data):
        unique_low_risk_ids = set(entry["track_id"] for entry in data if "track_id" in entry and entry.get("zone") == "low-risk")
        unique_high_risk_ids = set(entry["track_id"] for entry in data if "track_id" in entry and entry.get("zone") == "high-risk")
        return len(unique_low_risk_ids), len(unique_high_risk_ids)

    def display_risk_bar_chart(self, label, low_risk_count, high_risk_count, chart_placeholder):
        chart_data = pd.DataFrame({
            'Risk Level': ['Low Risk', 'High Risk'],
            'Count': [low_risk_count, high_risk_count]
        })
        chart_data = chart_data.set_index('Risk Level')
        chart_placeholder.bar_chart(chart_data, use_container_width=True)

    def check_new_threats(self, data):
        threats = [entry for entry in data if entry.get("suspicious_activity")]
        if threats:
            st.warning(f"New threats detected: {len(threats)}")
        return len(threats)
    

    
    
    def display_threat_image(self, data):
        st.subheader("Threat Profile")
        
        if st.session_state.current_index < len(st.session_state.unique_track_ids):
            track_id = st.session_state.unique_track_ids[st.session_state.current_index]
            threats = [entry for entry in data if entry["track_id"] == track_id]

            if threats:
                threat = threats[0]  # Assuming each track_id is unique in the data
                st.write("Zone:", threat['zone'])

                # Search for the image based on track_id prefix
                image_search_path = f"/Users/jarad/SMU SCHOOL/SW_ARCH/7319_Project/Main/MainProject/Crops/person/person_{threat['track_id']}.0_*png"
                matching_files = glob.glob(image_search_path)
                
                # If we found a matching image, display it
                if matching_files:
                    img = resize_image(matching_files[0], base_width=400)
                    st.image(img, caption=f"Image for Track ID: {threat['track_id']}", use_column_width=True)
                else:
                    st.warning(f"Image for Track ID {threat['track_id']} not found.")
        else:
            st.write("No more data available!")

    


    def update_dashboard(self):
        # Fetch data from the FastAPI service
        person_response = requests.get("http://localhost:8000/get_person_data/")
        person_data = person_response.json().get("data", [])
        
        col1, col2 = st.columns(2)

        with col1:
            # Display the last updated time
            st.write("Last updated at: ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

            # Display risk bar charts for person data
            person_low_risk, person_high_risk = self.get_risk_counts(person_data)
            self.display_risk_bar_chart("Person", person_low_risk, person_high_risk, st)
            
            threats_count = self.check_new_threats(person_data)
            st.write(f"Total Suspicious Activities: {threats_count}")

        with col2:
            # Fetch the specific threat data based on current_index
            if st.session_state.current_index < len(st.session_state.unique_track_ids):
                track_id = st.session_state.unique_track_ids[st.session_state.current_index]
                self.display_threat_image(person_data)

        # Navigation buttons
        with col1:
            if st.button('Previous', key="prev_btn") and st.session_state.current_index > 0:
                st.session_state.current_index -= 1
            if st.button('Next', key="next_btn") and st.session_state.current_index < len(st.session_state.unique_track_ids) - 1:
                st.session_state.current_index += 1
            

    def run_app(self):
        # self.initialize_data()
        st.title('Security Analysis Dashboard')
        
            # Button to start analysis
        if st.button('Start Analyzing'):
            self.initialize_data()
            
        self.update_dashboard()

if __name__ == "__main__":
    dashboard = StreamlitDashboard()
    dashboard.run_app()



