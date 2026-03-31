import cv2
import mediapipe as mp
import numpy as np
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arccos(
        np.dot(a - b, c - b) /
        (np.linalg.norm(a - b) * np.linalg.norm(c - b))
    )
    return np.degrees(radians)

cap = cv2.VideoCapture(0)

bad_posture_start = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

        ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]

        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        angle = calculate_angle(ear, shoulder, hip)

        if angle < 40:
            status = "Bad Posture"
            color = (0, 0, 255)

            if bad_posture_start is None:
                bad_posture_start = time.time()

            elapsed = time.time() - bad_posture_start

            if elapsed > 5:
                cv2.putText(frame, "ALERT! Fix Posture!", (30, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        else:
            status = "Good Posture"
            color = (0, 255, 0)
            bad_posture_start = None

        cv2.putText(frame, f'Angle: {int(angle)}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.putText(frame, status, (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Posture Analyzer", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
