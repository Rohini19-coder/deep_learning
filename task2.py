import cv2

# ---------------------------
# Load Haar Cascade for face detection
# ---------------------------
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# ---------------------------
# Function: Detect faces in an image
# ---------------------------
def detect_faces_in_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow('Detected Faces', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ---------------------------
# Function: Detect faces from webcam in real-time
# ---------------------------
def detect_faces_webcam():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imshow('Webcam Face Detection', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------------
# Main Program
# ---------------------------
print("Choose option:")
print("1. Detect faces in an image")
print("2. Detect faces using webcam")
choice = input("Enter 1 or 2: ")

if choice == '1':
    image_path = input("Enter image filename (with extension): ")
    detect_faces_in_image(image_path)
elif choice == '2':
    detect_faces_webcam()
else:
    print("Invalid choice")
