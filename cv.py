import cv2
import numpy as np
import asyncio
import websockets
import time


async def capture_frames_and_display():
    cap = cv2.VideoCapture(0)  # Use the default camera (change the index if needed)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Video Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


async def send_mean_color():
    print("executing")
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        while True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(now)
            await websocket.send(now)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(capture_frames_and_display(), send_mean_color())
    )
