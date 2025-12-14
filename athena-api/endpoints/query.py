from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.gemini_service import process_message

router = APIRouter()

class QueryRequest(BaseModel):
    prompt_msg: str
    context: str
    merchant_id: str

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        print("AJJAJAJAJAJAJAJAJAJAJA")
        result = await process_message(
            prompt_msg=request.prompt_msg,
            context=request.context,
            merchant_id=request.merchant_id
        )
        return result
    except Exception as e:
        print(f"Error in /query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
