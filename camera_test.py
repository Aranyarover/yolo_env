import cv2
import os
from datetime import datetime

# ============================================================
# ARANYA - Arducam HQ Camera Capture
# Raspberry Pi 4 + Ubuntu 22.04
# ============================================================

# Camera device
CAMERA_DEVICE = "/dev/video0"

# Folder where images will be saved
SAVE_FOLDER = "captured_images"

# Create folder if it doesn't exist
os.makedirs(SAVE_FOLDER, exist_ok=True)

print("========================================")
print(" ARANYA - Arducam HQ Camera")
print("========================================")

# ------------------------------------------------------------
# Open camera
# ------------------------------------------------------------

print("Opening camera:", CAMERA_DEVICE)

cap = cv2.VideoCapture(CAMERA_DEVICE, cv2.CAP_V4L2)

if not cap.isOpened():
    print("ERROR: Camera could not be opened")
    exit()

print("Camera device opened successfully!")

# ------------------------------------------------------------
# Set YUYV format
# ------------------------------------------------------------

fourcc = cv2.VideoWriter_fourcc(*"YUYV")
cap.set(cv2.CAP_PROP_FOURCC, fourcc)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set FPS
cap.set(cv2.CAP_PROP_FPS, 30)

print("Format: YUYV")
print("Resolution: 640 x 480")
print("FPS: 30")

# ------------------------------------------------------------
# Read first frame
# ------------------------------------------------------------

ret, frame = cap.read()

if not ret:
    print()
    print("========================================")
    print("ERROR: Failed to read camera frame!")
    print("========================================")
    print()
    print("Camera is detected but no image frame")
    print("was received from /dev/video0.")
    print()

    cap.release()
    exit()

print("First camera frame received successfully!")

# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------

print()
print("========================================")
print(" CAMERA RUNNING")
print("========================================")
print("Press 'c' = Capture image")
print("Press 'q' = Quit")
print("========================================")

while True:

    # Read frame
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Failed to read camera frame")
        break

    # Display live camera feed
    cv2.imshow("ARANYA - Arducam HQ Camera", frame)

    # Read keyboard
    key = cv2.waitKey(1) & 0xFF

    # --------------------------------------------------------
    # Capture image when 'c' is pressed
    # --------------------------------------------------------

    if key == ord("c"):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = os.path.join(
            SAVE_FOLDER,
            f"tree_{timestamp}.jpg"
        )

        success = cv2.imwrite(filename, frame)

        if success:
            print()
            print("IMAGE CAPTURED!")
            print("Saved:", filename)
            print()
        else:
            print("ERROR: Could not save image")

    # --------------------------------------------------------
    # Quit when 'q' is pressed
    # --------------------------------------------------------

    elif key == ord("q"):

        print()
        print("Closing camera...")
        break

# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------

cap.release()
cv2.destroyAllWindows()

print("Camera closed.")
print("Program finished.")

