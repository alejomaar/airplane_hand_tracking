import cv2
import numpy as np
import asyncio
import websockets

async def capture_frames_and_display():
    cap = cv2.VideoCapture(0)  # Use the default camera (change the index if needed)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        cv2.imshow('Video Stream', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

async def send_mean_color():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:
        cap = cv2.VideoCapture(0)  # Use the default camera (change the index if needed)
        
        while True:
            
            
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Calculate the mean color of the frame
            mean_color = np.mean(frame, axis=(0, 1))
            
            # Convert the mean color to a list for serialization
            mean_color = mean_color.tolist()
            
            # Send the mean color to the WebSocket server
            await websocket.send(str(mean_color))
    
        cap.release()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(asyncio.gather(capture_frames_and_display(), send_mean_color()))
