# import pickle
# import cv2

# def get_recognized_gesture(model, le, frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.resize(gray, (64, 64)).flatten()
#     prediction = model.predict([gray])
#     gesture = le.inverse_transform(prediction)[0]
#     return gesture

# # Load the model and label encoder
# with open('gesture_model.pkl', 'rb') as f:
#     model = pickle.load(f)
# with open('label_encoder.pkl', 'rb') as f:
#     le = pickle.load(f)

# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         gesture = get_recognized_gesture(model, le, frame)
        
#         # Store the recognized gesture in a variable and print it
#         recognized_gesture = gesture
#         print(f'Recognized Gesture: {recognized_gesture}')
        
#         cv2.putText(frame, f'Gesture: {recognized_gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#         cv2.imshow('Gesture Recognition', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np
# import tensorflow as tf
# import pickle

# def recognize_gesture():
#     # Load the trained model
#     model = tf.keras.models.load_model('gesture_model.h5')
    
#     # Load the label encoder
#     with open('label_encoder.pkl', 'rb') as f:
#         le = pickle.load(f)
    
#     cap = cv2.VideoCapture(0)
#     recognized_gesture = None  # Variable to store the recognized gesture

#     while True:
#         ret, frame = cap.read()
#         if ret:
#             frame = cv2.flip(frame, 1)  # Flip frame to avoid mirror effect
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             gray = cv2.resize(gray, (64, 64))
#             gray = np.expand_dims(gray, axis=-1)
#             gray = gray / 255.0  # Normalize pixel values
#             gray = np.expand_dims(gray, axis=0)

#             # Predict the gesture
#             prediction = model.predict(gray)
#             recognized_gesture = le.inverse_transform([np.argmax(prediction)])[0]

#             # Display the result
#             cv2.putText(frame, f'Gesture: {recognized_gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#             cv2.imshow('Gesture Recognition', frame)

#             # Print the recognized gesture
#             print(f'Recognized Gesture: {recognized_gesture}')

#             # Press 'q' to quit
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()
#     return recognized_gesture

# # Run real-time gesture recognition and print the result
# gesture = recognize_gesture()
# print(f'Final Recognized Gesture: {gesture}')

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

def recognize_gesture(landmarks):
    # Get coordinates of necessary landmarks
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    # Define simple rules for rock, paper, scissors
    if thumb_tip.y < index_tip.y:
        return "stone"
    elif thumb_tip.y > pinky_tip.y:
        return "paper"
    else:
        return "scissor"

def process_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            return recognize_gesture(landmarks)
    return None

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gesture = process_frame(frame)

    if gesture:
        print(f'Gesture: {gesture}')
        cv2.putText(frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
