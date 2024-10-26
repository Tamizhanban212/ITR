import cv2
import numpy as np
import tensorflow as tf
import pickle

def recognize_gesture():
    # Load the trained model
    model = tf.keras.models.load_model('gesture_model.h5')
    
    # Load the label encoder
    with open('label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    
    cap = cv2.VideoCapture(0)
    recognized_gesture = None  # Variable to store the recognized gesture

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Flip frame to avoid mirror effect
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (64, 64))
            gray = np.expand_dims(gray, axis=-1)
            gray = gray / 255.0  # Normalize pixel values
            gray = np.expand_dims(gray, axis=0)

            # Predict the gesture
            prediction = model.predict(gray)
            recognized_gesture = le.inverse_transform([np.argmax(prediction)])[0]

            # Display the result
            cv2.putText(frame, f'Gesture: {recognized_gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Gesture Recognition', frame)

            # Print the recognized gesture
            print(f'Recognized Gesture: {recognized_gesture}')

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return recognized_gesture

# Run real-time gesture recognition and print the result
gesture = recognize_gesture()
print(f'Final Recognized Gesture: {gesture}')
