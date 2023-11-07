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

The Smart home security system performs real-time video analytics on footage from cameras or local storage with ability detect and track people and vehicles, publishing the object data to an event bus that routes it to separate pipelines for customized threat analysis of humans and vehicles. These analytics pipelines identify potential security risks like loitering and unusual activities, sending alerts and images crops to a web dashboard that allows homeowners to monitor emerging threats on their property through an intuitive, centralized interface. It it currently set up to run on CPU to run on most consumer PCs

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
   - Download video here: https://drive.google.com/file/d/1V5nkxMUJhwXdAwm1Pi9ll5h2PaTAfCqx/view?usp=sharing

5. **Download the weights**:
   - The weights should downloand when ran if not download here: https://github.com/ultralytics/ultralytics

6. **Update the Configuration File**:
   - Update your configuration file as needed. 

7. **Run the Project**:
   ```bash
   cd Main/MainProject
   python main.py
   ```
8. **Stop the Project**:
   ```bash
   Cntrl + c 
   ```

---
## Architecture decision

- A traditional 3-tier architecture was considered as an alternative, structured with presentation, logic, and data tiers:

  - The presentation tier would contain the dashboard and visualizations.
  - The logic tier would handle components like the object detectors, classifiers, and analytics.
  - The data tier would include databases like PostgreSQL and blob stores for video.
  - Requests would flow sequentially through each tier. The presentation would send to logic, and logic would interact with data.
  - Tight dependencies between tiers since processing relies on waterfall flow.
  - Scaling by adding servers to each tier independently.
  - Centralized data storage even for large video assets.

- In contrast, the event-driven architecture has:

  - Decoupled components that communicate asynchronously via events. 
  - Parallel pipelines, with threat dataa streamed to analytics components.
  - No direct links between the dashboard, detectors, and databases.
  - Loose coupling allows scaling specific pieces like the DataProducer.
  - Video stored distributed on disk while metadata goes to databases.
  - Real-time processing versus batch windows.
  
For this video security application, an event-driven architecture fits best because:

- Only analyze threats when they occur and only run models based on rules.
- Video frames and detections need high-throughput streaming.  
- Loose coupling allows optimizing and hyperparamterizing of each analytics component.
- New analytics use cases can consume events easily.
- Decoupling person and vehicles allows for easier updates to new models.
- Central database limits scalability.
- Latency needs to be low for video processing.
- Decoupling with an event driven architecture allows for easily adding more cameras and scaling based on location.

- An event-driven approach provides the right architectural style for this video security application because of its need for high throughput streaming, loose coupling between components, low latency, and scalability. The video frames and object detections generated need to be processed at high speeds and volumes. An event architecture promotes the decoupled, parallel flows critical for performance. Additionally, employing an event-driven approach allows optimizing each component independently without tight dependencies. New detection models and threat logic can be easily added by having them consume events as needed. Events also enable low latency by allowing components to react in real-time versus waiting on batch processing. Scaling horizontally across cameras and locations can be achieved by adding instances of components like DataProducer. The loose coupling and horizontal scalability are key benefits of using an event-driven architecture versus a 3 tiered architecture.
---

---

## Changes to Proposed Architecture

I changed the location of saving threat images to the local file system and not using a database for these reasons:
      - When in actual use the video files are large raw streams, not structured data needed for queries.
      - Low latency access to the videos is needed for real-time processing. File system is better optimized for this.
      - Storing on disk allows easier sharing of the video storage across nodes if needed.
      - Retaining only relevant threat clips rather than all footage is simpler when separated from database.

## Future Enhancements

1. **Additional Model Integration**: Implement  ML algorithms for better threat detection including facial recognition and license plate reader.
2. **Cloud Integration**: Enable cloud storage for storing footage and analysis.
  
---




