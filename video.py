import websockets
import asyncio
import cv2
from config.settings import settings
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

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


def log_attempt_number(retry_state):
    """return the result of the last call attempt"""
    logging.error(f"Retrying: {retry_state.attempt_number}...")


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(10),
    reraise=True,
    after=log_attempt_number,
)
async def main():
    await asyncio.create_task(streaming())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt")
