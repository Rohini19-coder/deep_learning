import cv2
import time

# ---------------------------
# Universal Tracker Creator
# ---------------------------
def create_tracker(tracker_type="CSRT"):
    """
    Create an OpenCV tracker that works with both old (≤4.5.x)
    and new (≥4.10.x) versions.
    """
    tracker = None
    tracker_type = tracker_type.upper()

    try:
        if tracker_type == "CSRT":
            if hasattr(cv2, "TrackerCSRT_create"):  
                tracker = cv2.TrackerCSRT_create()
            elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerCSRT_create"):  # new API
                tracker = cv2.legacy.TrackerCSRT_create()
            elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerCSRT"):  # fallback
                tracker = cv2.legacy.TrackerCSRT().create()

        elif tracker_type == "KCF":
            if hasattr(cv2, "TrackerKCF_create"):
                tracker = cv2.TrackerKCF_create()
            elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerKCF_create"):  # new API
                tracker = cv2.legacy.TrackerKCF_create()
            elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerKCF"):  # fallback
                tracker = cv2.legacy.TrackerKCF().create()

        else:
            print(f" Tracker type '{tracker_type}' not supported in this OpenCV build.")

    except Exception as e:
        print(f" Error creating tracker: {e}")

    return tracker


video_path = input("Enter video filename (with extension) or '0' for webcam (press Enter for webcam): ").strip()

if video_path == "" or video_path == "0":
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(" Error: Cannot open video or webcam")
    exit()

# ---------------------------
# Initialize Tracker
# ---------------------------
tracker = create_tracker("CSRT")

if tracker is None:
    print(" Could not create tracker. Try another type or reinstall OpenCV.")
    exit()
else:
    print(" Tracker created successfully!")

ret, frame = cap.read()
if not ret:
    print("Error: Cannot read video frame")
    exit()

# ---------------------------
# Select ROI
# ---------------------------
print("👉 Draw a box around the object, then press ENTER or SPACE. Press 'c' to cancel.")

# Resize frame for ROI window (so it fits nicely)
frame_resized = cv2.resize(frame, (640, 480))
bbox = cv2.selectROI("Select Object to Track", frame_resized, False)

if bbox == (0, 0, 0, 0):
    print(" Error: No ROI selected. Exiting...")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Scale ROI back to original frame size
fx = frame.shape[1] / 640
fy = frame.shape[0] / 480
x, y, w, h = bbox
bbox = (int(x * fx), int(y * fy), int(w * fx), int(h * fy))

tracker.init(frame, bbox)
cv2.destroyWindow("Select Object to Track")

# ---------------------------
# Setup Resizable Window
# ---------------------------
cv2.namedWindow("Object Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Object Tracking", 640, 480)  # adjust window size here

# ---------------------------
# Tracking Loop
# ---------------------------
screenshot_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cv2.putText(frame, "Tracking", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),4)
    else:
        cv2.putText(frame, "Lost", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    # Resize for display
    frame_disp = cv2.resize(frame, (640, 480))
    cv2.imshow("Object Tracking", frame_disp)

    # Key controls
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # save screenshot
        filename = f"screenshot_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved as {filename}")

    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
