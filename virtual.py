import cv2
import numpy as np
import pyautogui
import sys
import time

# Disable fail-safe to prevent immediate boundary crashes
pyautogui.FAILSAFE = False

# Initialize webcam with an extra delay for Mac hardware to wake up
cap = cv2.VideoCapture(0)
time.sleep(1.0) 

if not cap.isOpened():
    print("Trying alternate camera index...")
    cap = cv2.VideoCapture(1)

# Get your MacBook screen size
screen_width, screen_height = pyautogui.size()

# Define HSV color range (Bright Blue)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

print("==============================================")
print("📸 Camera initialized successfully!")
print("👉 Keep a bright blue object ready in frame.")
print("👉 Press 'q' inside the camera window to exit.")
print("==============================================")

while True:
    ret, frame = cap.read()
    
    # If the Mac drops a single frame, don't let the whole program crash
    if not ret:
        continue

    # Flip the frame horizontally for natural mirroring
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # Clean up image noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        if cv2.contourArea(largest_contour) > 500:
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                # Draw tracking dot
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                # Map coordinates proportionally 
                screen_x = int(cx * (screen_width / w))
                screen_y = int(cy * (screen_height / h))

                try:
                    pyautogui.moveTo(screen_x, screen_y, duration=0.01)
                except:
                    pass

    # Show the window
    cv2.imshow("Mac Virtual Mouse", frame)

    # CRUCIAL FOR MAC: A slightly longer wait key ensures the window stays open
    key = cv2.waitKey(30) & 0xFF
    if key == ord('q') or key == 27: # 'q' or ESC key to quit
        break

cap.release()
cv2.destroyAllWindows()
# Mac cleanup force
for i in range(5):
    cv2.waitKey(1)
