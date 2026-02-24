import cv2
import numpy as np
import math

class HandGestureRecognizer:
    def __init__(self):
        # Simple gesture mapping
        self.gesture_names = {
            'FIST': {'name': 'Fist', 'emoji': '👊'},
            'OPEN_PALM': {'name': 'Open Palm', 'emoji': '✋'},
            'THUMBS_UP': {'name': 'Thumbs Up', 'emoji': '👍'},
            'THUMBS_DOWN': {'name': 'Thumbs Down', 'emoji': '👎'},
            'PEACE': {'name': 'Peace', 'emoji': '✌️'},
            'OKAY': {'name': 'Okay', 'emoji': '👌'},
            'UNKNOWN': {'name': 'Unknown', 'emoji': '🖐️'}
        }
        
        self.action_map = {
            'FIST': 'Mute',
            'OPEN_PALM': 'Stop',
            'THUMBS_UP': 'Volume Up',
            'THUMBS_DOWN': 'Volume Down',
            'PEACE': 'Play/Pause',
            'OKAY': 'Confirm'
        }
        
        # For smoothing
        self.prev_gesture = 'UNKNOWN'
        self.gesture_count = 0
        self.stable_gesture = 'UNKNOWN'
        self.stable_threshold = 5
        
        # For demonstration, we'll cycle through gestures
        self.demo_gestures = ['FIST', 'OPEN_PALM', 'THUMBS_UP', 'PEACE', 'OKAY']
        self.demo_index = 0
        self.demo_counter = 0
        
        print(" Gesture recognizer initialized (Demo Mode)")
    
    def process_frame(self, frame):
        """
        Process a single frame and return annotated image with gesture info
        This is a demo version that cycles through gestures
        """
        try:
            if frame is None:
                return frame, {'hands_detected': 0, 'gestures': [], 'stable_gesture': None}
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Get frame dimensions
            h, w, _ = frame.shape
            
            # Draw a hand detection box (simulating detection)
            center_x, center_y = w // 2, h // 2
            box_size = 200
            
            cv2.rectangle(frame, 
                         (center_x - box_size//2, center_y - box_size//2),
                         (center_x + box_size//2, center_y + box_size//2),
                         (0, 255, 0), 2)
            
            # Demo mode: cycle through gestures every 30 frames
            self.demo_counter += 1
            if self.demo_counter > 30:
                self.demo_counter = 0
                self.demo_index = (self.demo_index + 1) % len(self.demo_gestures)
            
            current_demo_gesture = self.demo_gestures[self.demo_index]
            
            # For demo, always say hands are detected
            gesture_results = {
                'hands_detected': 1,
                'gestures': [{
                    'name': self.gesture_names[current_demo_gesture]['name'],
                    'emoji': self.gesture_names[current_demo_gesture]['emoji']
                }],
                'stable_gesture': {
                    'name': self.gesture_names[current_demo_gesture]['name'],
                    'emoji': self.gesture_names[current_demo_gesture]['emoji'],
                    'action': self.action_map.get(current_demo_gesture, 'No Action')
                }
            }
            
            # Draw the gesture on frame
            gesture_info = self.gesture_names[current_demo_gesture]
            display_text = f"{gesture_info['emoji']} {gesture_info['name']}"
            
            # Add background for text
            cv2.rectangle(frame, 
                         (center_x - box_size//2, center_y - box_size//2 - 30),
                         (center_x - box_size//2 + 200, center_y - box_size//2),
                         (0, 0, 0), -1)
            
            cv2.putText(frame, display_text, 
                       (center_x - box_size//2 + 5, center_y - box_size//2 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Add instructions
            cv2.putText(frame, "Demo Mode - Cycling Gestures", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            return frame, gesture_results
            
        except Exception as e:
            print(f"Process error: {e}")
            return frame, {'hands_detected': 0, 'gestures': [], 'stable_gesture': None}