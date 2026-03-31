# Screen Time Posture Analyzer

## Problem
Many students develop poor posture while using laptops, leading to long-term health issues.

## Solution
This project uses computer vision to detect posture in real time and alert users when they maintain bad posture for too long.

## Features
- Real-time posture detection
- Angle calculation using body landmarks
- Alert system
- Visual feedback

## Tech Stack
- Python
- OpenCV
- MediaPipe
- NumPy

## How It Works
- The system uses MediaPipe to detect body landmarks
- Key points like ear, shoulder, and hip are extracted
- The angle between these points is calculated
- If the angle is below a threshold, posture is classified as bad
- If bad posture continues for a few seconds, an alert is triggered

## How to Run
```bash
pip install -r requirements.txt
python main.py


