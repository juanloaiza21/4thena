from fastapi import APIRouter, HTTPException
from service.mongo_service import getContractMessages

router = APIRouter()

@router.post("/contract")
async def contract_endpoint(merchant_id: str):
    try:
        results = getContractMessages(merchant_id=merchant_id)
        # Convert ObjectId to str if necessary, but assuming pymongo returns usable dicts.
        # If _id follows ObjectId, it might break JSON serialization.
        # Let's clean up results just in case.
        cleaned_results = []
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            cleaned_results.append(doc)
            
        return cleaned_results
    except Exception as e:
        print(f"Error in /contract: {e}")
        raise HTTPException(status_code=500, detail=str(e))
