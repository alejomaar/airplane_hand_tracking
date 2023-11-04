from fastapi import FastAPI, WebSocket

app = FastAPI()

# WebSocket URL to forward messages


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
