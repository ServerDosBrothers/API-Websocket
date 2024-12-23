from fastapi import APIRouter, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import websockets, isConnected
from ..logger import logger

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

@router.post("/{client}", status_code=201)
async def create_message(client: str, message: Message):
    json=message.model_dump()
    for clientws in websockets:
        if clientws == client:
            continue
        json=message.model_dump()
        json["event_type"] = "message"
        
        try:
            await websockets[clientws]["ws"].send_json(json)
        except RuntimeError:
            logger.info(f"Envio pro cliente websocket {clientws} falhou, tornando a conexão como desconectada...")
            websockets[clientws]["connected"] = False
            
    recipients=isConnected(websockets)
    return {
            "message": message.model_dump(),
            "recipients": recipients          
            }
        
        
