import cv2
import numpy as np

# Define a function to identify color and coordinates
def detect_blocks(frame):
    # Convert the image to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges for blocks (you can adjust these ranges)
    color_ranges = {
        "red": ((0, 120, 70), (10, 255, 255)),   # Lower and upper bounds for red
        "green": ((36, 50, 70), (89, 255, 255)), # Lower and upper bounds for green
        "blue": ((90, 50, 70), (128, 255, 255)), # Lower and upper bounds for blue
        # Add other colors as needed
    }

    detected_blocks = []

    for color_name, (lower, upper) in color_ranges.items():
        # Create masks for the color
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filter small contours
            if cv2.contourArea(contour) < 500:  # Adjust threshold as necessary
                continue

            # Get the bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Get the center of the block
            cx = x + w // 2
            cy = y + h // 2

            # Draw a rectangle and label the block
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(frame, f"{color_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Append detected block details
            detected_blocks.append({
                "color": color_name,
                "coordinates": (cx, cy)
            })

    return frame, detected_blocks

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect blocks and their colors
    processed_frame, blocks = detect_blocks(frame)

    # Display detected blocks in the console
    for block in blocks:
        print(f"Detected {block['color']} block at {block['coordinates']}")

    # Show the processed frame
    cv2.imshow("Block Detection", processed_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
