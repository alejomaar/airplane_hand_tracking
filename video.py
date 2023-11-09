import websockets
import asyncio
import cv2
from config.settings import settings

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)


async def streaming():
    # Connect to the server
    async with websockets.connect(
        f"{settings.ws_host_server}/ws", open_timeout=settings.ws_timeout
    ) as ws:
        while True:
            success, frame = camera.read()
            if not success:
                camera.release()
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                camera.release()
                break
            else:
                ret, buffer = cv2.imencode(".png", frame)
                await ws.send(buffer.tobytes())


async def main():
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            await asyncio.create_task(streaming())
        except Exception as e:
            print(f"Retrying service ({retry_count + 1}/{max_retries})")
            await asyncio.sleep(settings.ws_timeout)
            retry_count += 1
    print("The connection could not be established")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt")
