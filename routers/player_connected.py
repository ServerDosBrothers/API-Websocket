from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import connected
import starlette

router = APIRouter(
    prefix="/pc",
    tags=["player_connected"],
    responses={404: {"message":"This request was invalid"}},
)

class PlayerConnected(BaseModel):
    name: str
    steamid: str
    country: str
    
@router.post("/")
async def create_message(player_connected: PlayerConnected):
    for clientws in connected:
        if clientws == "tf2":
            continue    
        await connected[clientws].send_json(player_connected.model_dump_json())