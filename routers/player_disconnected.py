from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import connected
from ..dependencies import get_token_header
import starlette

router = APIRouter(
    prefix="/pd",
    tags=["player_disconnected"],
    responses={404: {"message":"This request was invalid"}},
)

class PlayerDisconnected(BaseModel):
    name: str
    steamid: str
    reason: str
    
@router.post("/")
async def create_message(player_disconnected: PlayerDisconnected):
    for clientws in connected:
        if clientws == "tf2":
            continue    
        await connected[clientws].send_json(player_disconnected.model_dump_json())