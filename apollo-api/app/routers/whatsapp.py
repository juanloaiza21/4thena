from fastapi import APIRouter, HTTPException
from app.services.gemini_service import gemini_service
import random

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Sample phone numbers for mock data
CLIENT_PHONE_NUMBERS = [
    {"number": "573174799575@c.us", "name": "Mike", "company": "TechFlow"},
    {"number": "573105767451@c.us", "name": "Sarah", "company": "PayMaster"},
    {"number": "573001234567@c.us", "name": "Carlos", "company": "QuickBuy"},
    {"number": "573009876543@c.us", "name": "Emma", "company": "NovaPay"},
    {"number": "573112233445@c.us", "name": "David", "company": "FinTech Solutions"},
]

YUNO_PHONE = {"number": "573000000000@c.us", "name": "Yuno Support"}

@router.get("/messages")
async def get_messages(count: int = 5):
    """
    Get mock WhatsApp conversation with both client inquiries and Yuno responses.
    """
    try:
        # Generate conversation messages using Gemini
        conversation = await gemini_service.generate_whatsapp_messages(count)
        
        messages = []
        for msg in conversation:
            is_yuno_response = msg.get("is_yuno", False)
            
            if is_yuno_response:
                # Message from Yuno
                client = random.choice(CLIENT_PHONE_NUMBERS)
                messages.append({
                    "text": msg.get("text", ""),
                    "source": "whatsapp",
                    "from": YUNO_PHONE["number"],
                    "from_name": YUNO_PHONE["name"],
                    "to": client["number"],
                    "to_name": client["name"],
                    "is_yuno_response": True
                })
            else:
                # Message from client
                client = random.choice(CLIENT_PHONE_NUMBERS)
                messages.append({
                    "text": msg.get("text", ""),
                    "source": "whatsapp",
                    "from": client["number"],
                    "from_name": client["name"],
                    "from_company": client["company"],
                    "to": YUNO_PHONE["number"],
                    "to_name": YUNO_PHONE["name"],
                    "is_yuno_response": False
                })
        
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
