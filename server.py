from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import websockets
from numpy.typing import NDArray
from numpy import uint8
import json
from services import HandTracking, Movement

app = FastAPI()
hand_tracking = HandTracking()
movement_x = Movement()
movement_y = Movement()


def decode_image(img_bytes: bytes) -> NDArray[uint8]:
    arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return frame


def show_video_streaming(frame: NDArray[uint8]):
    cv2.imshow("frame", frame)
    cv2.waitKey(1)


def get_dynamics_from_tracking(frame: NDArray[uint8]):
    hand_tracking.find_hand(frame)
    hand_vector = hand_tracking.find_main_keypoint(frame, False)
    if hand_vector is None:
        return None
    (hand_x, hand_y) = hand_vector
    movement_x.update_dynamics(hand_x)
    movement_y.update_dynamics(hand_y)

    if movement_x.denoised_velocity is None or movement_y.denoised_velocity:
        return None

    return dict(
        x=hand_x,
        y=hand_y,
        vx=movement_x.denoised_velocity,
        vy=movement_y.denoised_velocity,
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # listen for connections
    await websocket.accept()
    forward_websocket = await websockets.connect("ws://localhost:8001/unity")
    try:
        while True:
            img_bytes = await websocket.receive_bytes()
            frame = decode_image(img_bytes)
            dynamics = get_dynamics_from_tracking(frame)
            
            encode_msg = json.dumps(dynamics)

            await forward_websocket.send(encode_msg)
    except WebSocketDisconnect:
        cv2.destroyWindow("frame")
        print("Client disconnected")
