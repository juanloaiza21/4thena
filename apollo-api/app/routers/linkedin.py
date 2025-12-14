from fastapi import APIRouter, HTTPException
from app.services.gemini_service import gemini_service
import random

router = APIRouter(prefix="/linkedin", tags=["linkedin"])

# Sample LinkedIn profile URLs for mock data
LINKEDIN_PROFILES = [
    {"id": "john-smith-techflow", "name": "John Smith", "company": "TechFlow"},
    {"id": "maria-garcia-paymaster", "name": "Maria Garcia", "company": "PayMaster"},
    {"id": "carlos-ruiz-quickbuy", "name": "Carlos Ruiz", "company": "QuickBuy"},
    {"id": "sarah-johnson-novapay", "name": "Sarah Johnson", "company": "NovaPay"},
    {"id": "david-chen-fintech", "name": "David Chen", "company": "FinTech Solutions"},
]

YUNO_PROFILE = {"id": "yuno-payments", "name": "Yuno Payments", "company": "Yuno"}

@router.get("/messages")
async def get_messages(count: int = 5):
    """
    Get mock LinkedIn messages with conversation between clients and Yuno.
    Includes both client inquiries and Yuno responses.
    """
    try:
        # Generate conversation messages using Gemini
        conversation = await gemini_service.generate_linkedin_conversation(count)
        
        messages = []
        for msg in conversation:
            is_yuno_response = msg.get("is_yuno", False)
            
            if is_yuno_response:
                # Message from Yuno
                client_profile = random.choice(LINKEDIN_PROFILES)
                messages.append({
                    "text": msg.get("text", ""),
                    "source": "linkedin",
                    "from": YUNO_PROFILE["id"],
                    "from_name": YUNO_PROFILE["name"],
                    "to": client_profile["id"],
                    "to_name": client_profile["name"],
                    "is_yuno_response": True
                })
            else:
                # Message from client
                client_profile = random.choice(LINKEDIN_PROFILES)
                messages.append({
                    "text": msg.get("text", ""),
                    "source": "linkedin",
                    "from": client_profile["id"],
                    "from_name": client_profile["name"],
                    "from_company": client_profile["company"],
                    "to": YUNO_PROFILE["id"],
                    "to_name": YUNO_PROFILE["name"],
                    "is_yuno_response": False
                })
        
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
