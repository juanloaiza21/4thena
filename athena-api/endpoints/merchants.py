from fastapi import APIRouter, HTTPException
from service.mongo_service import getMerchants

router = APIRouter()

@router.post("/merchants")
async def query_endpoint():
    try:
        return getMerchants()
    except Exception as e:
        print(f"Error in /query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
