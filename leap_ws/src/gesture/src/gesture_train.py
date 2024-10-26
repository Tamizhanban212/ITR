# import os
# import cv2
# import numpy as np
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import accuracy_score

# X, y = [], []

# # Load and preprocess data
# def load_data():
#     for gesture in ['stone', 'paper', 'scissor']:
#         for img_name in os.listdir(f'/home/tamizhanban/Documents/ITR/leap_ws/src/gesture/data/{gesture}'):
#             img_path = f'/home/tamizhanban/Documents/ITR/leap_ws/src/gesture/data/{gesture}/{img_name}'
#             img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#             if img is None:
#                 print(f"Warning: Could not read image {img_path}")
#                 continue
#             img = cv2.resize(img, (64, 64))  # Resize to consistent size
#             img = img.flatten()  # Flatten to 1D array
#             X.append(img)
#             print(img)
#             y.append(gesture)
#     return np.array(X), np.array(y)

# # Train model
# X, y = load_data()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# le = LabelEncoder()
# y_train_enc = le.fit_transform(y_train)
# y_test_enc = le.transform(y_test)

# model = SVC(kernel='linear')
# model.fit(X_train, y_train_enc)

# # Evaluate model
# y_pred = model.predict(X_test)
# print('Accuracy:', accuracy_score(y_test_enc, y_pred))

# # Save the model
# import pickle
# with open('gesture_model.pkl', 'wb') as f:
#     pickle.dump(model, f)
# with open('label_encoder.pkl', 'wb') as f:
#     pickle.dump(le, f)

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

# Load and preprocess data
def load_data():
    X, y = [], []
    for gesture in ['stone', 'paper', 'scissor']:
        for img_name in os.listdir(f'/home/tamizhanban/Documents/ITR/leap_ws/src/gesture/data/{gesture}'):
            img_path = f'/home/tamizhanban/Documents/ITR/leap_ws/src/gesture/data/{gesture}/{img_name}'
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Warning: Could not read image {img_path}")
                continue
            img = cv2.resize(img, (64, 64))  # Resize to consistent size
            img = np.expand_dims(img, axis=-1)  # Add channel dimension
            X.append(img)
            y.append(gesture)
    return np.array(X), np.array(y)

# Load data
X, y = load_data()

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.4, random_state=42)

# Normalize data
X_train, X_test = X_train / 255.0, X_test / 255.0

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(le.classes_), activation='softmax')
])

# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, validation_split=0.2)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print('Accuracy:', accuracy)

# Save the model and label encoder
model.save('gesture_model.h5')
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)