import cv2
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Load Image
# ---------------------------
image_path = input("Enter image filename (with extension): ")
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
    exit()

# Resize image for easier display
image = cv2.resize(image, (600, 400))

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ---------------------------
# Function for nothing (used in trackbars)
# ---------------------------
def nothing(x):
    pass

# ---------------------------
# Create Window and Trackbars
# ---------------------------
cv2.namedWindow('Canny Edge Detection', cv2.WINDOW_NORMAL)  # Use WINDOW_NORMAL
cv2.createTrackbar('Threshold1', 'Canny Edge Detection', 100, 500, nothing)
cv2.createTrackbar('Threshold2', 'Canny Edge Detection', 200, 500, nothing)

# ---------------------------
# Edge Detection Loop
# ---------------------------
while True:
    t1 = cv2.getTrackbarPos('Threshold1', 'Canny Edge Detection')
    t2 = cv2.getTrackbarPos('Threshold2', 'Canny Edge Detection')

    # Apply Canny edge detection
    edges = cv2.Canny(gray, t1, t2)

    # Display original and edges side by side
    combined = np.hstack((cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                          cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)))
    cv2.imshow('Canny Edge Detection', combined)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# ---------------------------
# Optional: Display using Matplotlib
# ---------------------------
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title('Original Grayscale')
plt.imshow(gray, cmap='gray')

plt.subplot(1,2,2)
plt.title('Edges')
plt.imshow(edges, cmap='gray')

plt.show()
