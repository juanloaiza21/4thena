from fastapi import APIRouter, Request, Form, Response
from app.services.twilio_service import twilio_service
from pydantic import BaseModel

router = APIRouter(prefix="/calls", tags=["calls"])

class CallRequest(BaseModel):
    to_number: str
    webhook_url: str 

@router.post("/start")
async def start_call(request: CallRequest):
    """
    Initiates an outbound call to the specified number.
    The webhook_url will be called by Twilio when the call is answered.
    """
    try:
        call = twilio_service.make_call(request.to_number, request.webhook_url)
        return {"call_sid": call.sid, "status": call.status}
    except Exception as e:
        from fastapi import HTTPException
        print(f"Error making call: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def call_webhook(request: Request):
    """
    Webhook endpoint handled by Twilio.
    Returns TwiML instructions for the call.
    """
    # Twilio sends data as form-urlencoded
    form_data = await request.form()
    
    # You can access call details from form_data (e.g., CallSid, From, To)
    # print(form_data) 
    
    twiml = twilio_service.generate_twiml_for_call("Hello! This call is being recorded. Please modify this message in the endpoint.")
    
    return Response(content=twiml, media_type="application/xml")

@router.post("/status")
async def call_status(request: Request):
    """
    Webhook for call status updates (completed, failed, etc.) if configured in Twilio.
    """
    form_data = await request.form()
    # Log status or update DB
    print(f"Call Status Update: {form_data.get('CallStatus')}")
    return {"status": "received"}

@router.post("/recording")
async def call_recording(request: Request):
    """
    Webhook for recording completion. Twilio sends the RecordingUrl here.
    """
    form_data = await request.form()
    recording_url = form_data.get("RecordingUrl")
    print(f"✅ Recording Available at: {recording_url}")
    return {"status": "received"}

@router.get("/recordings")
async def list_recordings():
    """
    List recent recordings from Twilio.
    """
    recordings = twilio_service.list_recordings()
    return recordings

@router.get("/token")
async def get_access_token(identity: str = "user"):
    """
    Generate an Access Token for Twilio Client (Browser).
    """
    token = twilio_service.create_access_token(identity)
    return {"token": token, "identity": identity}

@router.post("/outgoing-browser")
async def outgoing_browser_call(request: Request):
    """
    TwiML App webhook. Called when browser initiates a call.
    Expects 'To' in the form data.
    """
    form_data = await request.form()
    to_number = form_data.get("To") # The number the browser wants to call
    
    if not to_number:
        # If no number, maybe just playing a message or default
        response = Response(content="<Response><Say>No number provided</Say></Response>", media_type="application/xml")
        return response

    twiml = twilio_service.generate_twiml_for_browser_outbound(to_number)
    return Response(content=twiml, media_type="application/xml")

class JoinMeetingRequest(BaseModel):
    phone_number: str  # The dial-in number for the meeting
    pin: str  # The meeting ID/PIN (include # if needed)

@router.post("/join-meeting")
async def join_meeting(request: JoinMeetingRequest):
    """
    Join a Google Meet or Teams meeting via dial-in and record it.
    """
    from app.core.config import settings
    try:
        webhook_url = f"{settings.NGROK_URL}/calls/meeting-twiml"
        call = twilio_service.join_meeting(request.phone_number, request.pin, webhook_url)
        return {"call_sid": call.sid, "status": call.status, "message": "Joining meeting..."}
    except Exception as e:
        from fastapi import HTTPException
        print(f"Error joining meeting: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/meeting-twiml")
async def meeting_twiml(request: Request, pin: str = ""):
    """
    TwiML webhook for meeting dial-in. Sends the PIN as DTMF tones.
    """
    twiml = twilio_service.generate_twiml_for_meeting(pin)
    return Response(content=twiml, media_type="application/xml")
