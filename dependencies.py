from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

async def get_token_header(token: Annotated[str, Header()]):
    if token != str(os.getenv("API_TOKEN")):
        raise HTTPException(status_code=400, detail="X-Token header invalid")