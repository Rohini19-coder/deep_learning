import cv2

# Ask user for image or webcam
choice = input("Enter '1' to scan QR from image or '2' to use webcam: ")

if choice == '1':
    image_path = input("Enter image filename (with extension): ")
    img = cv2.imread(image_path)
    if img is None:
        print(" Could not open image. Check the file path.")
        exit()

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None:
        # Draw bounding box
        n_lines = len(bbox)
        for i in range(n_lines):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i+1) % n_lines][0]))
            cv2.line(img, pt1, pt2, color=(0, 255, 0), thickness=2)

    if data:
        print("QR Code Data:", data)
    else:
        print(" No QR code detected.")

    cv2.imshow("QR Code Scanner", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

elif choice == '2':
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Failed to read from webcam.")
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            n_lines = len(bbox)
            for i in range(n_lines):
                pt1 = tuple(map(int, bbox[i][0]))
                pt2 = tuple(map(int, bbox[(i+1) % n_lines][0]))
                cv2.line(frame, pt1, pt2, color=(0, 255, 0), thickness=2)

        if data:
            cv2.putText(frame, data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

else:
    print("Invalid choice. Enter 1 or 2.")
