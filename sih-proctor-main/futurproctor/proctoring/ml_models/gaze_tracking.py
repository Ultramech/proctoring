import cv2
import numpy as np
# Initialize MediaPipe Face Mesh lazily
mp_face_mesh = None
face_mesh = None

def load_face_mesh():
    global mp_face_mesh, face_mesh
    if face_mesh is None:
        import mediapipe as mp
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
    return face_mesh

def gaze_tracking(frame):
    """Detect gaze direction (left, right, center)."""
    # Ensure model is loaded
    mesh = load_face_mesh()
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            # Get left and right eye landmarks
            left_eye = [landmarks.landmark[33], landmarks.landmark[159]]  # Left eye corners
            right_eye = [landmarks.landmark[362], landmarks.landmark[386]]  # Right eye corners

            # Calculate horizontal gaze direction
            left_eye_center = np.mean([(p.x, p.y) for p in left_eye], axis=0)
            right_eye_center = np.mean([(p.x, p.y) for p in right_eye], axis=0)

            gaze_direction = "center"
            if left_eye_center[0] < 0.4:  # Left threshold
                gaze_direction = "left"
            elif right_eye_center[0] > 0.6:  # Right threshold
                gaze_direction = "right"

            return {"gaze": gaze_direction}

    return {"gaze": "center"}