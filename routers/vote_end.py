from fastapi import APIRouter, Depends, HTTPException, WebSocket
from pydantic import BaseModel
from .websocket import connected
from ..dependencies import get_token_header
import starlette

router = APIRouter(
    prefix="/ve",
    tags=["vote_end"],
    responses={404: {"message":"This request was invalid"}},
)

class VoteEnd(BaseModel):
    next_map: str

@router.post("/")
async def create_message(vote_end: VoteEnd):
    for clientws in connected:
        if clientws == "tf2":
            continue    
        await connected[clientws].send_json(vote_end.model_dump_json())