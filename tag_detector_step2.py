import cv2
from pyapriltags import apriltags

import capnp # pip3 install pycapnp
capnp.add_import_hook(['./capnp'])

import tagdetection_capnp as TagDetection
import image_capnp as Image

import numpy as np

import ecal.core.core as ecal_core

import sys
# from capnp_subscriber import CapnpSubscriber
from capnp_publisher import CapnpPublisher


# visualisation deps
import rerun as rr

def main():


    print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
    
    # initialize eCAL API
    ecal_core.initialize(sys.argv, "tag_detector_pub")
    
    # set process state
    ecal_core.set_process_state(1, 1, "I feel good")

    # initialise visualiser
    rr.init("rerun_tag_detector")
    rr.spawn(memory_limit="1GB")


    detector = apriltags.Detector(families='tag16h5')

    # Open the webcam (you may need to adjust the camera index)
    cap = cv2.VideoCapture(0)

    pub = CapnpPublisher("S0/cama/tags", "TagDetections")
    pubImage = CapnpPublisher("S0/cama", "Image")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the image
        detections = detector.detect(gray)

        # Draw bounding boxes around detected tags
        msg = TagDetection.TagDetections.new_message()

        num_detections = 0
        for detection in detections:
            if detection.hamming > 0:
                continue
            num_detections += 1

        tags = msg.init('tags', num_detections)

        msg.image.width = frame.shape[1]
        msg.image.height = frame.shape[0]

        msgImage = Image.Image.new_message()
        msgImage.width = frame.shape[1]
        msgImage.height = frame.shape[0]
        # data = msgImage.init('data', len(frame))
        # data = frame
        msgImage.data = frame.tobytes()
        msgImage.encoding = Image.Image.Encoding.bgr8
        msgImage.mipMapLevels = 0

        # convert from OpenCV BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rr.log("webcam/image", rr.Image(frame_rgb))

        count = 0
        corners_list = list()
        ids_list = list()
        for detection in detections:
            if detection.hamming > 0:
                continue
            # print(detection.tag_id)
            # print(detection.corners)
            corners_list.append(np.vstack([detection.corners, detection.corners[0, :]]))
            ids_list.append(detection.tag_id)

            cv2.polylines(frame, [detection.corners.astype(int)], True, (0, 255, 0), 2)

            # Draw the corners of the tag
            for corner in detection.corners:
                cv2.circle(frame, tuple(corner.astype(int)), 5, (0, 0, 255), -1)

            np_corners = np.array(detection.corners)

            # print(frame.shape)
            # (height, width, channel)

            np_corners[:, 0] /= frame.shape[1]
            np_corners[:, 1] /= frame.shape[0]


            print(np_corners)
            tags[count].id = detection.tag_id
            tags[count].pointsPolygon = np.array(detection.corners).flatten().tolist()
            tags[count].family = TagDetection.TagFamily.tag16h5

            count += 1

        # logging to visualiser, with ability to show labels for each tag id
        rr.log("webcam/tags", rr.LineStrips2D(corners_list, labels=ids_list))

        pub.send(msg.to_bytes())
        pubImage.send(msgImage.to_bytes())

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