from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .websocket import connected
from ..dependencies import get_token_header
import starlette

router = APIRouter(
    prefix="/mc",
    tags=["map_change"],
    responses={404: {"message":"This request was invalid"}},
)

class MapChange(BaseModel):
    did_map_end: bool
    map_name: str

@router.post("/")
async def create_message(map_change: MapChange):
    for clientws in connected:
        if clientws == "tf2":
            continue    
        await connected[clientws].send_json(map_change.model_dump_json())