from flask import Flask, render_template, Response, jsonify, request
import cv2
import time

from gesture_utils import HandGestureRecognizer

app = Flask(__name__)

# Global variables
camera = None
is_camera_active = False
current_frame = None
recognizer = HandGestureRecognizer()

def generate_frames():
    
    global camera, is_camera_active, current_frame, recognizer
    
    while True:
        if camera is not None and is_camera_active:
            success, frame = camera.read()
            if success:
                # Process frame
                processed_frame, _ = recognizer.process_frame(frame)
                current_frame = processed_frame
                
                # Encode
                ret, buffer = cv2.imencode('.jpg', processed_frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                time.sleep(0.01)
        else:
            time.sleep(0.01)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera, is_camera_active
    
    try:
        if camera is not None:
            camera.release()
            camera = None
            time.sleep(0.5)
        
    
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            return jsonify({'success': False, 'message': 'Could not open camera'})
        
      
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        

        ret, frame = camera.read()
        if not ret:
            return jsonify({'success': False, 'message': 'Could not read from camera'})
        
        is_camera_active = True
        print("Camera started successfully")
        
        return jsonify({'success': True, 'message': 'Camera started'})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera, is_camera_active
    
    if camera is not None:
        camera.release()
        camera = None
    
    is_camera_active = False
    print(" Camera stopped")
    return jsonify({'success': True})

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_frame', methods=['POST'])
def capture_frame():
    """Get current gesture results"""
    global current_frame, recognizer, is_camera_active
    
    if not is_camera_active:
        return jsonify({'success': False, 'message': 'Camera not active'})
    
    if current_frame is None:
        return jsonify({'success': False, 'message': 'No frame available'})
    
    try:
        _, gesture_results = recognizer.process_frame(current_frame)
        return jsonify({'success': True, 'gesture_results': gesture_results})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_gestures')
def get_gestures():
    """Get list of available gestures"""
    gestures = []
    for key, value in recognizer.gesture_names.items():
        if key != 'UNKNOWN':
            gestures.append({
                'name': value['name'],
                'emoji': value['emoji'],
                'action': recognizer.action_map.get(key, 'No Action')
            })
    return jsonify({'gestures': gestures})

if __name__ == '__main__':
    print(" Starting GestureAI server...")
    print(" Templates folder:", app.template_folder)
    print(" Visit: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)