from fastapi import APIRouter, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import connected


class Message(BaseModel):
    user: str
    content: str
    steamid: str
    team: str

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
        json=message.model_dump()
        json["event_type"] = "message"
        await connected[clientws].send_json(json)
