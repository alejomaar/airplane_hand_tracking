import asyncio
from fastapi import FastAPI, WebSocket
import websockets

app = FastAPI()

# WebSocket URL to forward messages
forward_uri = "ws://localhost:8001/ws"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Incoming websocket connection established")
    # Establish a connection to the target WebSocket server (Service C)
    
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")
            
            # Forward the received message to another WebSocket server (Service C)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()

@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Incoming websocket connection established")
    # Establish a connection to the target WebSocket server (Service C)
    forward_websocket = await websockets.connect(forward_uri)
    print("forwarding websocket connection established")
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")
            
            # Forward the received message to another WebSocket server (Service C)
            await forward_websocket.send(message)
    except Exception as e:
        print(e)
    finally:
        await forward_websocket.close()
        await websocket.close()
