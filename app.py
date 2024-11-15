# application.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

@app.get("/")
def health_check():
    return {"Hello": "World"}

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            print(f'HEY {message}')
            # Broadcast message to all other clients
            for connection in active_connections:
                await connection.send_text(message)  # Include a message prefix for clarity
    except WebSocketDisconnect:
        # Remove client from active connections on disconnect
        print(f'Removing {websocket}')
        active_connections.remove(websocket)
        await websocket.close()
