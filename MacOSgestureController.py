import cv2
import mediapipe as mp
import numpy as np
import sys
import osascript
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

start = input("Press [1] to start the program or Press [2] to view instructions: ")

if(start == 2):
    print('Instructions:')

if(start == '1'):
    print("press [q] to quit at any time.")
    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle


    # Setup mediapipe instance
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0
    stage = None
    command = ''

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame - cv2.flip(frame,-1)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates of different body parts
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                leftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                rightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                leftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                rightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                leftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                rightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                leftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                rightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                leftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                rightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                         landmarks[mp_pose.PoseLandmark.NOSE.value].y]



                # Calculate angles
                leftBicepCurlAngle = calculate_angle(leftShoulder, leftElbow, leftWrist)
                rightBicepCurlAngle = calculate_angle(rightShoulder, rightElbow, rightWrist)
                leftLegCurlAngle = calculate_angle(leftHip, leftKnee, leftAnkle)
                rightLegCurlAngle = calculate_angle(rightHip, rightKnee, rightAnkle)

                # PLAY Command Logic
                if leftBicepCurlAngle > 160:
                    stage = "downArmLeft"
                if leftBicepCurlAngle < 30:
                    command = 'PLAY'
                    osascript.osascript('tell application "music" to play')

                # PAUSE Command Logic
                if rightBicepCurlAngle > 160:
                    stage = "downArmRight"
                if rightBicepCurlAngle < 30:
                    command = 'PAUSE'
                    osascript.osascript('tell application "music" to pause')

                # VOLUME 100 Command Logic
                if leftLegCurlAngle > 160:
                    stage = "downLegLeft"
                if leftLegCurlAngle < 100:
                    command = 'VOLUME 100'
                    osascript.osascript('set volume output volume 100')

                # VOLUME 0 Command Logic
                if rightLegCurlAngle > 160:
                    stage = "downLegRight"
                if rightLegCurlAngle < 100:
                    command = 'VOLUME 0'
                    osascript.osascript('set volume output volume 0')

                # OPEN MUSIC Command Logic
                if rightBicepCurlAngle < 90 and leftBicepCurlAngle < 90:
                    command = 'OPEN MUSIC'
                    if(counter%2==0):
                        osascript.osascript('tell application "music" to activate')
                    else:
                        osascript.osascript('quit app "music.app"')
                    counter += 1


            except:
                pass

            # Show Command
            cv2.putText(image, 'Command',
                        (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, command,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Output Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
