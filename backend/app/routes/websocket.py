from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

active_connections = []

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):

    await websocket.accept()

    active_connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            for connection in active_connections:
                await connection.send_text(
                    f"New Notification: {data}"
                )

    except WebSocketDisconnect:
        active_connections.remove(websocket)