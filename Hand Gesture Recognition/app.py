import cv2
import mediapipe as mp
import math
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Futuristic HUD Colors (Neon Cyan and Purple)
NEON_CYAN = (255, 255, 0) # BGR
NEON_PURPLE = (255, 0, 255)

def calculate_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Futuristic Overlay: Grid Lines
        cv2.line(frame, (0, h//2), (w, h//2), (0, 50, 0), 1)
        cv2.line(frame, (w//2, 0), (w//2, h), (0, 50, 0), 1)

        gesture = "SYSTEM STANDBY"
        color = NEON_CYAN

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get coordinates for Thumb (4), Index (8), Middle (12)
                landmarks = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((cx, cy))
                
                if len(landmarks) > 0:
                    thumb_tip = landmarks[4]
                    index_tip = landmarks[8]
                    middle_tip = landmarks[12]
                    
                    # Draw Futuristic Reticle on Index Finger
                    cv2.circle(frame, index_tip, 15, NEON_PURPLE, 2)
                    cv2.circle(frame, index_tip, 2, NEON_CYAN, cv2.FILLED)

                    # Logic: Pinch (Click)
                    if calculate_distance(thumb_tip, index_tip) < 40:
                        gesture = "TARGET ENGAGED (PINCH)"
                        color = (0, 0, 255) # Red alert
                        cv2.line(frame, thumb_tip, index_tip, color, 3)
                        
                    # Logic: Peace Sign (Scan Mode)
                    elif calculate_distance(index_tip, middle_tip) > 60 and calculate_distance(thumb_tip, index_tip) > 100:
                        gesture = "SCANNING MODE (PEACE)"
                        color = NEON_PURPLE
                        
                    # Logic: Open Palm
                    else:
                        gesture = "PALM DETECTED"

                # Draw standard landmarks but with neon colors
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                      mp_draw.DrawingSpec(color=NEON_PURPLE, thickness=2, circle_radius=2),
                                      mp_draw.DrawingSpec(color=NEON_CYAN, thickness=2, circle_radius=2))

        # Add HUD Text
        cv2.putText(frame, f"STATUS: {gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Convert to jpeg for web streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)