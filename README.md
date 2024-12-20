# E.D.I.T.H.

## Overview
E.D.I.T.H. (Enhanced Driver Intervention and Traffic Handling) is a comprehensive driver assistance system designed to enhance road safety by simultaneously detecting driver drowsiness and monitoring lane positions. In case of detecting drowsiness, E.D.I.T.H. triggers an alarm, reduces the vehicle's speed, and navigates it safely to the side lane.

## Features
- **Driver Drowsiness Detection:** Utilizes computer vision and machine learning techniques to monitor the driver's eye movements and facial expressions.
- **Lane Detection:** Continuously monitors lane markings to ensure the vehicle remains within its designated lane.
- **Safety Protocols:** On detecting drowsiness, it triggers alarms, decelerates the vehicle, and steers it to a safe stop by the side of the road.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SanidhyaMishra1808/E.D.I.T.H.git
    cd E.D.I.T.H
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. To start the system, run the main script:
    ```bash
    python src/main.py
    ```

2. The system will begin monitoring for drowsiness and lane positioning. Ensure your camera is connected and properly positioned.

## Drowsiness Detection
- The `drowsiness_detection.py` script uses OpenCV and Dlib to monitor the driver’s eyes and facial landmarks.
- A pre-trained machine learning model is used to analyze these inputs and detect signs of drowsiness.

## Lane Detection
- The `lane_detection.py` script employs computer vision techniques to identify lane markings using the vehicle's camera feed.
- The script ensures the vehicle remains centered within its lane and provides real-time feedback.

## Testing
To run tests, use the following command:
```bash
pytest


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SanidhyaMishra1808/E.D.I.T.H.git
    cd E.D.I.T.H
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. To start the system, run the main script:
    ```bash
    python src/main.py
    ```

2. The system will begin monitoring for drowsiness and lane positioning. Ensure your camera is connected and properly positioned.

## Drowsiness Detection
- The `drowsiness_detection.py` script uses OpenCV and Dlib to monitor the driver’s eyes and facial landmarks.
- A pre-trained machine learning model is used to analyze these inputs and detect signs of drowsiness.

## Lane Detection
- The `lane_detection.py` script employs computer vision techniques to identify lane markings using the vehicle's camera feed.
- The script ensures the vehicle remains centered within its lane and provides real-time feedback.

## Testing
To run tests, use the following command:
```bash
pytest
