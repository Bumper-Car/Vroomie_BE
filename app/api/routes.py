from fastapi import APIRouter

from app.api import websocket
from app.schemas.message import ChatRequest, ChatResponse
from app.services.assistant import get_gpt_response

router = APIRouter()
router.include_router(websocket.router)

@router.post("/ask", response_model=ChatResponse)
async def ask(req: ChatRequest):
    answer = await get_gpt_response(req.message)
    return ChatResponse(reply=answer)
