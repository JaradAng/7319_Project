# Smart Home Video Security System - README

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Data Producer](#data-producer)
4. [Event Bus](#event-bus)
5. [Person and Vehicle Pipelines](#person-and-vehicle-pipelines)
6. [Threat Analysis](#threat-analysis)
7. [Dashboard](#dashboard)
8. [Technologies Used](#technologies-used)
9. [Installation and Setup](#installation-and-setup)
10. [Future Enhancements](#future-enhancements)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

This application serves as a comprehensive smart home video security system. It is designed to consume and process video footage, track objects within the frame, analyze for threats, and display the analyzed data on a user-friendly dashboard.

---

---
## Installation and Setup

## How to Run

Follow the steps below to set up and run the project:

1. **Clone the Repository**: (Assumption: You have a git repository for the project)
   ```bash
   git clone [Your Repository URL]
   cd [Your Repository Name]
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Your Video**:
   - Place your `.mp4` video in the `input_media` directory.

5. **Update the Configuration File**:
   - Rename your configuration file as needed. (Assumption: The name you're changing it to is based on some criteria, possibly the name of the video or a specific configuration.)

6. **Run the Project**:
   ```bash
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
---

## Future Enhancements

1. **Additional Model Integration**: Implement  ML algorithms for better threat detection including facial recognition and license plate reader.
2. **Cloud Integration**: Enable cloud storage for storing footage and analysis.
  
---




