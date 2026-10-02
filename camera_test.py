import cv2
import os
from datetime import datetime

# Adjust this if v4l2-ctl showed a different primary node (e.g., 0, 2, or 4)
CAMERA_INDEX = 0

SAVE_FOLDER = "captured_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Initialize the standard V4L2 backend
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)

# Force MJPEG format to prevent USB bottlenecking on the Pi
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
# 1080p resolution (or lower to 1280x720 if YOLO needs faster framerates)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("ERROR: Cannot open the Brio 100. Check the CAMERA_INDEX.")
    exit()

print("==============================================")
print(" ARANYA - LOGITECH BRIO 100 STREAM ACTIVE")
print(" Press 'c' to Capture | Press 'q' to Quit")
print("==============================================")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream disconnected.")
        break

    # ====================================================
    # Pass 'frame' directly to your YOLOv8 model here
    # ====================================================

    cv2.imshow("Plant Vision Stream", frame)
   
    key = cv2.waitKey(1) & 0xFF
   
    if key == ord('c'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(SAVE_FOLDER, f"tree_{timestamp}.jpg")
        cv2.imwrite(filepath, frame)
        print(f"Captured: {filepath}")
       
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
