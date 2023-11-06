from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import websockets
app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # listen for connections
    await websocket.accept()
    forward_websocket = await websockets.connect('ws://localhost:8001/unity')
    try:
        while True:
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
            msg = str(np.mean(frame))
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            print(msg)
            await forward_websocket.send(msg)
    except WebSocketDisconnect:
        cv2.destroyWindow("frame")
        print("Client disconnected")


