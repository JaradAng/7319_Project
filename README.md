# Smart Home Video Security System - README

## Table of Contents

1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Data Producer](#data-producer)
4. [Architecture decision](#Architecture-decision)
5. [Changes to Proposed Architecture](#chages-to-proposed-architecture)
6. [Future Enhancements](#future-enhancements)


---

## Overview

This application serves as a comprehensive smart home video security system. It is designed to consume and process video footage, track objects within the frame, analyze for threats, and display the analyzed data on a user-friendly dashboard. It it currently set up to run on CPU to run on most consumer PCs

---

---
## Installation and Setup

## How to Run

Follow the steps below to set up and run the project:

1. **Clone the Repository**: (Assumption: You have a git repository for the project)
   ```bash
   git clone CS5-7319-Final-Project-Group-01-Jarad-Angel
   cd CS5-7319-Final-Project-Group-01-Jarad-Angel
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Your Video**:
   - Place your `.mp4` video in the `input_media` directory.

5. **Download the weights**:
   - The weights should downloand when ran if not download here: https://github.com/ultralytics/ultralytics

6. **Update the Configuration File**:
   - Update your configuration file as needed. 

7. **Run the Project**:
   ```bash
   cd Main/MainProject
   python main.py
   ```


---
## Architecture decision

For this video security application, an event-driven architecture fits best because:

- Only analyze threats when they occur and only run models based on rules.
- Video frames and detections need high-throughput streaming.
- Loose coupling allows optimizing and hyperparamterizing of each analytics   component.
- New analytics use cases can consume events easily.
- Decoupling person and vehicles allows for easier updates to new models.
- Central database limits scalability.
- Latency needs to be low for video processing.
- Decoupling with an event driven architecture allows for easily adding more  cameras and scaling based on location. 


An event-driven approach provides the right architectural style for this video security application because of its need for high throughput streaming, loose coupling between components, low latency, and scalability. The video frames and object detections generated need to be processed at high speeds and volumes. An event architecture promotes the decoupled, parallel flows critical for performance. Additionally, employing an event-driven approach allows optimizing each component independently without tight dependencies. New detection models and threat logic can be easily added by having them consume events as needed. Events also enable low latency by allowing components to react in real-time versus waiting on batch processing. Scaling horizontally across cameras and locations can be achieved by adding instances of components like DataProducer. The loose coupling and horizontal scalability are key benefits of using an event-driven architecture versus a 3 tiered architecture.
---

---

## Changes to Proposed Architecture
- I changed the location of saving threat images to the local file system and not using a database for these reasons:
      - When in actual use the video files are large raw streams, not structured data needed for queries.
      - Low latency access to the videos is needed for real-time processing. File system is better optimized for this.
      - Storing on disk allows easier sharing of the video storage across nodes if needed.
      - Retaining only relevant threat clips rather than all footage is simpler when separated from database.

## Future Enhancements

1. **Additional Model Integration**: Implement  ML algorithms for better threat detection including facial recognition and license plate reader.
2. **Cloud Integration**: Enable cloud storage for storing footage and analysis.
  
---




