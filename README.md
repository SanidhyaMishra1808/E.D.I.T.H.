# E.D.I.T.H.

## Overview
E.D.I.T.H. (Enhanced Driver Interface for Transcendent Heuristics) is a comprehensive driver assistance system designed to enhance road safety by simultaneously detecting driver drowsiness and monitoring lane positions. In case of detecting drowsiness, E.D.I.T.H. triggers an alarm, reduces the vehicle's speed, and navigates it safely to the side lane.

## Features
- **Driver Drowsiness Detection:** Utilizes computer vision and machine learning techniques to monitor the driver's eye movements and facial expressions.
- **Lane Detection:** Continuously monitors lane markings to ensure the vehicle remains within its designated lane.
- **Safety Protocols:** On detecting drowsiness, it triggers alarms, decelerates the vehicle, and steers it to a safe stop by the side of the road.

## System Requirements
- Operating System: Windows, macOS, or Linux
- Python 3.6 or higher
- Webcam for real-time monitoring
- Speaker for alarm sound
- traffic video file named spv


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/SanidhyaMishra1808/E.D.I.T.H.git
    cd E.D.I.T.H
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the necessary system dependencies:**

   - On Ubuntu:
     ```bash
     sudo apt-get update
     sudo apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
     ```

   - On Windows, make sure you have Visual Studio installed.

## Requirements File

Make sure your `requirements.txt` includes the following dependencies:
face_recognition, opencv-python, pygame, scipy, numpy.


## Running the Project

1. **Start the system:**
    - Open PowerShell (Windows) or Terminal (macOS/Linux).
    - Navigate to the project directory:
      ```bash
      cd path_to_your_project/E.D.I.T.H
      ```
    - Run the main script:
      ```bash
      python src/main.py
      ```

2. **Usage:**
    - The system will begin monitoring for drowsiness and lane positioning.
    - Ensure your camera is connected and properly positioned.
    - Press 'q' to exit the application.

## Drowsiness Detection
- The `drowsiness_detection.py` script uses OpenCV and face_recognition to monitor the driver’s eyes and facial landmarks.
- A pre-trained machine learning model is used to analyze these inputs and detect signs of drowsiness.

## Lane Detection
- The `lane_detection.py` script employs computer vision techniques to identify lane markings using the vehicle's camera feed.
- The script ensures the vehicle remains centered within its lane and provides real-time feedback.

## Testing
To run tests, use the following command:
```bash
pytest
```
