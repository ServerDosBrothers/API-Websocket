from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
import starlette.websockets

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
    responses={404: {"message":"This request was invalid"}},
)

connected={}

@router.websocket("/{client}")
async def websocket_endpoint(client: str, websocket: WebSocket):
    await websocket.accept()
    connected[client]=websocket
    while True:
        try:
            data=await websocket.receive_json()
        except starlette.websockets.WebSocketDisconnect as e:
            print(f"Websocket desconectou: {e}")
            del connected[client]
