from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.services.meetingbaas_service import meetingbaas_service
from app.core.config import settings

router = APIRouter(prefix="/meet", tags=["meet"])

class JoinMeetRequest(BaseModel):
    meeting_url: str  # Google Meet URL
    bot_name: str = "Apollo Recorder"

@router.post("/join")
async def join_meet(request: JoinMeetRequest):
    """
    Send a bot to join a Google Meet and record it.
    """
    try:
        webhook_url = f"{settings.NGROK_URL}/meet/webhook" if settings.NGROK_URL else None
        result = await meetingbaas_service.join_meet(
            meeting_url=request.meeting_url,
            bot_name=request.bot_name,
            webhook_url=webhook_url
        )
        return result
    except Exception as e:
        print(f"Error joining meet: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bots")
async def list_bots():
    """
    List all active bots.
    """
    try:
        return await meetingbaas_service.list_bots()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bots/{bot_id}")
async def get_bot(bot_id: str):
    """
    Get status of a specific bot.
    """
    try:
        return await meetingbaas_service.get_bot(bot_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/bots/{bot_id}")
async def delete_bot(bot_id: str):
    """
    Remove a bot from a meeting.
    """
    try:
        return await meetingbaas_service.delete_bot(bot_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def meet_webhook(request: Request):
    """
    Webhook for Meeting BaaS events (recording ready, etc.)
    """
    data = await request.json()
    print(f"📹 Meeting BaaS Webhook: {data}")
    
    # Handle different event types
    event_type = data.get("event")
    if event_type == "complete":
        print(f"✅ Recording ready: {data.get('mp4')}")
    
    return {"status": "received"}

@router.get("/bots/{bot_id}/recording")
async def get_recording(bot_id: str):
    """
    Get recording URLs for a completed meeting.
    Returns video (mp4), audio (mp3), and transcription URLs if available.
    """
    try:
        bot_data = await meetingbaas_service.get_bot(bot_id)
        data = bot_data.get("data", {})
        
        if data.get("status") != "completed":
            return {
                "status": data.get("status"),
                "message": "Recording not ready yet. Wait for status 'completed'.",
                "bot_id": bot_id
            }
        
        return {
            "bot_id": bot_id,
            "status": data.get("status"),
            "video_url": data.get("video"),
            "audio_url": data.get("audio"),
            "transcription_url": data.get("transcription"),
            "duration_seconds": data.get("duration_seconds"),
            "participants": data.get("participants", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recordings")
async def list_recordings():
    """
    List all completed recordings with their URLs.
    """
    try:
        bots_response = await meetingbaas_service.list_bots()
        bots = bots_response.get("data", [])
        
        recordings = []
        for bot in bots:
            if bot.get("status") == "completed":
                recordings.append({
                    "bot_id": bot.get("bot_id"),
                    "meeting_url": bot.get("meeting_url"),
                    "video_url": bot.get("video"),
                    "audio_url": bot.get("audio"),
                    "transcription_url": bot.get("transcription"),
                    "duration_seconds": bot.get("duration_seconds"),
                    "created_at": bot.get("created_at")
                })
        
        return {"recordings": recordings, "count": len(recordings)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
