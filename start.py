import asyncio
import websockets

async def connect_to_existing_websocket_server():
    uri = "ws://localhost:8000/ws"
    
    
    async with websockets.connect(uri) as websocket:
        # Perform WebSocket operations here
        await websocket.send("Hello, WebSocket Server!")
        await asyncio.sleep(10)
        await websocket.send("Hello, WebSocket Server!2 ")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect_to_existing_websocket_server())
