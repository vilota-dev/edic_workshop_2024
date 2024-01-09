import cv2
from pyapriltags import apriltags


def main():
    detector = apriltags.Detector(families='tag16h5')

    # Open the webcam (you may need to adjust the camera index)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the image
        detections = detector.detect(gray)

        # Draw bounding boxes around detected tags
        for detection in detections:
            if detection.hamming > 0:
                continue
            print(detection.tag_id)
            print(detection.corners)

            cv2.polylines(frame, [detection.corners.astype(int)], True, (0, 255, 0), 2)

            # Draw the corners of the tag
            for corner in detection.corners:
                cv2.circle(frame, tuple(corner.astype(int)), 5, (0, 0, 255), -1)

        # Display the resulting frame
        cv2.imshow('AprilTag Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()