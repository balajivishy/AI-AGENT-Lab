import cv2
import webbrowser
import time

# Load model
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)

# Class names from the MobileNet-SSD model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor", "laptop", "mouse",
           "remote", "keyboard", "cell phone", "microwave", "oven",
           "toaster", "sink", "refrigerator", "book", "clock", "vase",
           "scissors", "teddy bear", "hair drier", "toothbrush"]

PHONE_CLASS_ID = CLASSES.index("cell phone")

# To prevent opening the video multiple times
video_played = False  
youtube_link = "https://www.youtube.com/shorts/PAATsWOh8NQ"   # your link

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare frame for detection
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    phone_detected = False

    # Loop through detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])

        if confidence > 0.50 and class_id == PHONE_CLASS_ID:
            phone_detected = True
            # Draw bounding box
            box = detections[0, 0, i, 3:7] * \
                  [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (x1, y1, x2, y2) = box.astype("int")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "PHONE DETECTED", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # If phone detected, open YouTube link once
    if phone_detected and not video_played:
        print("PHONE DETECTED")
        webbrowser.open(youtube_link)
        video_played = True
        time.sleep(1)

    cv2.imshow("Phone Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
