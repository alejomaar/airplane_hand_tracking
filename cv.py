import websockets
import asyncio
import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

async def main():
    # Connect to the server
    async with websockets.connect('ws://localhost:8000/ws') as ws:
         while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.png', frame)
                await ws.send(buffer.tobytes())

# Start the connection
asyncio.run(main())