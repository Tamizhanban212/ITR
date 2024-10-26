import cv2
import numpy as np
import time

# Capture images for training
def capture_gesture_data(gesture_name, num_samples=100):
    cap = cv2.VideoCapture(0)
    i = 0
    start_time = time.time()

    while i < num_samples:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Flip frame to avoid mirror effect
            cv2.imshow('Capture Gesture Data', frame)
            
            current_time = time.time()
            if current_time - start_time >= 0.25:  # Capture every 0.5 seconds
                cv2.imwrite(f'/home/tamizhanban/Documents/ITR/leap_ws/src/gesture/data/{gesture_name}/{gesture_name}_{i}.jpg', frame)
                i += 1
                start_time = current_time  # Reset start time
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Capture data for three gestures
capture_gesture_data('paper')
# capture_gesture_data('stone')
capture_gesture_data('scissor')
