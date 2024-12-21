from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import connected
from ..dependencies import get_token_header
import starlette


class Message(BaseModel):
    user: str
    content: str
    steamid: str

router = APIRouter(
    prefix="/cm",
    tags=["message"],
    responses={404: {"message":"This request was invalid"}},
)

@router.post("/{client}")
async def create_message(client: str, message: Message):
    for clientws in connected:
        if clientws == client:
            continue
        
        await connected[clientws].send_json(message.model_dump_json())