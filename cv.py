import cv2
import numpy as np
import asyncio
import websockets


async def connect_to_existing_websocket_server():
    uri = "ws://localhost:8000/ws"
    cap = cv2.VideoCapture(0)  # Use the default camera (change the index if needed)

    async with websockets.connect(uri) as websocket:
        # Perform WebSocket operations here
        for i in range(100):
            ret, frame = cap.read()
            if not ret:
                print("Error reading")
                break
            mean = str(frame.mean())
            cv2.imshow("Video Stream", frame)
            await websocket.send(f"Hello, WebSocket Server{mean}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_to_existing_websocket_server())
