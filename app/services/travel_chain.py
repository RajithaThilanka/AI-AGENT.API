from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
import json
from typing import List, Dict, Any
import ast

from app.core.config import settings

class TravelAssistantChain:
    def __init__(self, llm):
        self.llm = llm
        
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
        )
        
        travel_prompt = PromptTemplate(
            template="""You are a travel assistant for Classic Travel.
            You help customers with air tickets, visa information, insurance, transportation, and accommodation.
            Your responses should be helpful, friendly, and concise.
            When speaking with a new customer, ask for their name and contact information before proceeding with their travel inquiry.
            
            Current conversation:
            {chat_history}
            
            Customer: {input}
            Travel Assistant:""",
            input_variables=["chat_history", "input"],
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=travel_prompt,
            memory=self.memory,
            verbose=True,
        )
    
    async def execute(self, input: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        # Initialize memory with previous messages if any
        if chat_history and len(chat_history) > 0 and len(self.memory.chat_memory.messages) == 0:
            for msg in chat_history:
                await self.memory.save_context(
                    {"input": msg["content"]},
                    {"output": msg.get("response", "")}
                )
        
        return await self.chain.acall({"input": input})
    
    async def generate_quick_replies(self, last_response: Dict[str, Any]) -> List[str]:
        # Generate contextually relevant quick replies based on conversation stage
        quick_reply_prompt = PromptTemplate(
            template="""Based on the following response from a travel assistant, generate 3-5 likely next queries or options the customer might want to select. Return only the options as a JSON array of strings.
            
            Travel Assistant's last response: {response}
            
            Quick reply options (JSON array):""",
            input_variables=["response"],
        )
        
        quick_reply_chain = LLMChain(
            llm=self.llm,
            prompt=quick_reply_prompt,
        )
        
        result = await quick_reply_chain.acall({
            "response": last_response["output"]
        })
        
        try:
            # Try to parse the result as JSON
            quick_replies = json.loads(result["text"])
            return quick_replies
        except json.JSONDecodeError:
            try:
                # Try to parse with ast.literal_eval if JSON parsing fails
                quick_replies = ast.literal_eval(result["text"])
                if isinstance(quick_replies, list):
                    return quick_replies
            except:
                pass
                
            print("Failed to parse quick replies:", result["text"])
            # Fallback options
            return ["Air tickets", "Visa", "Insurance", "Accommodation"]

# Dependency for FastAPI
def get_travel_chain():
    llm = ChatOpenAI(
        temperature=settings.TEMPERATURE,
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.MODEL_NAME,
    )
    return TravelAssistantChain(llm)