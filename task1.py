import cv2
import numpy as np

# ---------------------------
# Define HSV color ranges
# ---------------------------

# Red (two ranges because red wraps around HSV hue)
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Green
lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])

# Blue
lower_blue = np.array([94, 80, 2])
upper_blue = np.array([126, 255, 255])

# Dictionary to store colors and their ranges
colors = {
    'Red': [(lower_red1, upper_red1), (lower_red2, upper_red2)],
    'Green': [(lower_green, upper_green)],
    'Blue': [(lower_blue, upper_blue)]
}

# ---------------------------
# Start Webcam
# ---------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # optional

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, ranges in colors.items():
        # Combine masks if multiple ranges exist
        mask = None
        for lower, upper in ranges:
            temp_mask = cv2.inRange(hsv, lower, upper)
            if mask is None:
                mask = temp_mask
            else:
                mask = cv2.bitwise_or(mask, temp_mask)

        # Bitwise-AND mask with original frame
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # filter small objects
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, color_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    # Display frames
    cv2.imshow('Original', frame)
    cv2.imshow('Detected Colors', result)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
