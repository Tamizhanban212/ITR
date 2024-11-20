import cv2
import numpy as np

def detect_large_rectangle(frame):
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold to detect edges
    _, thresh = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    frame_area = frame.shape[0] * frame.shape[1]
    large_rect_corners = []

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the polygon is a rectangle (4 points)
        if len(approx) == 4:
            area = cv2.contourArea(contour)

            # Check if the rectangle occupies more than 75% of the frame area
            if area > 0.75 * frame_area:
                # Draw the rectangle
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)

                # Extract corner points
                corners = approx.reshape(4, 2)  # Reshape to (4, 2)
                for corner in corners:
                    cv2.circle(frame, tuple(corner), 5, (0, 0, 255), -1)

                # Save the corner coordinates
                large_rect_corners.append(corners)

    return frame, large_rect_corners


# Initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

readings = []  # Store readings of rectangle coordinates

while len(readings) < 20:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect large rectangle
    processed_frame, corners_list = detect_large_rectangle(frame)

    # If a large rectangle is found, store its coordinates
    if corners_list:
        for corners in corners_list:
            readings.append(corners)

    # Show the processed frame
    cv2.imshow("Large Rectangle Detection", processed_frame)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Compute average coordinates of the rectangle's corners
if readings:
    readings_array = np.array(readings)  # Convert to numpy array
    avg_coordinates = np.mean(readings_array, axis=0)  # Average across all readings
    print("Average Rectangle Coordinates (x, y):")
    for i, coord in enumerate(avg_coordinates):
        print(f"Corner {i + 1}: {coord}")

# Release resources
cap.release()
cv2.destroyAllWindows()
