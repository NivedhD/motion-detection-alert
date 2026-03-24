import cv2
import time
import glob
import os
from datetime import datetime
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1
image_with_object = None
clean_thread = None

def clean_folder():
    print("Cleaning up the folder...")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("Folder cleaned.")

def send_and_clean(image_path):
    send_email(image_path)
    clean_folder()

os.makedirs("images", exist_ok=True)

while True:
    status = 0
    check, frame = video.read()

    if not check or frame is None:
        print("Failed to read frame from camera.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"images/{timestamp}_{count}.png"
            cv2.imwrite(image_path, frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_text = "Motion Detected" if status == 1 else "No Motion"
    color = (0, 0, 255) if status == 1 else (0, 255, 0)
    cv2.putText(frame, f"Status: {status_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, time_text, (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    status_list.append(status)
    status_list = status_list[-2:]

    if len(status_list) == 2 and status_list[0] == 1 and status_list[1] == 0:
        if image_with_object:
            thread = Thread(target=send_and_clean, args=(image_with_object,))
            thread.daemon = True
            thread.start() 

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

if clean_thread is not None:
    clean_thread = Thread(target=clean_folder)
    clean_thread.start()