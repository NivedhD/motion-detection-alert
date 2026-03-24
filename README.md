# Motion Detection Camera

A Python app that detects motion via webcam and sends an 
email alert with an image attachment when motion is detected.

## Features
- Real-time motion detection using OpenCV
- Draws bounding boxes around detected objects
- Sends email with captured image when motion stops
- Auto-cleans saved images after sending

## Setup
1. Clone the repo
2. pip install opencv-python python-dotenv
3. Create a `.env` file
4. Generate a Gmail App Password at 
   myaccount.google.com → Security → App Passwords
5. Add your credentials to `.env`

## Usage
python main.py
Press `q` to quit.
