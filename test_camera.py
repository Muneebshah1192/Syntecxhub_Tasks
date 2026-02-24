import cv2
import time

print("📸 Simple Camera Test")
print("Press 'q' to quit, 's' to save image")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ Failed to open camera")
    exit()

print("✅ Camera opened successfully")
print(f"📊 Resolution: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if ret:
        frame_count += 1
        # Add text to frame
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Camera Test', frame)
        
        if frame_count % 30 == 0:  # Print every 30 frames
            print(f"✅ Captured {frame_count} frames")
    else:
        print("❌ Failed to capture frame")
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite(f"test_frame_{frame_count}.jpg", frame)
        print(f"💾 Saved frame {frame_count}")

cap.release()
cv2.destroyAllWindows()
print("🎉 Test complete")