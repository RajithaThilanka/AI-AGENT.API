from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.services.travel_chain import TravelAssistantChain, get_travel_chain

router = APIRouter()

class Message(BaseModel):
    content: str
    response: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

class ChatResponse(BaseModel):
    message: str
    quickReplies: List[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, travel_chain: TravelAssistantChain = Depends(get_travel_chain)):
    try:
        # Process message through LangChain
        response = await travel_chain.execute(
            input=request.message,
            chat_history=request.history
        )
        
        # Generate quick reply options based on context
        quick_replies = await travel_chain.generate_quick_replies(response)
        
        return ChatResponse(
            message=response["output"],
            quickReplies=quick_replies
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")