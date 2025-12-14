from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from app.core.config import settings

class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.phone_number = settings.TWILIO_PHONE_NUMBER

    def make_call(self, to_number: str, webhook_url: str):
        call = self.client.calls.create(
            to=to_number,
            from_=self.phone_number,
            url=webhook_url,
            record=True
        )
        return call

    def generate_twiml_for_call(self, message: str = "This call is being recorded for quality assurance. Please speak after the beep."):
        response = VoiceResponse()
        response.say(message)
        response.record(max_length=120, play_beep=True, action='/calls/recording')
        response.hangup()
        return str(response)

    def list_recordings(self, limit: int = 20):
        recordings = self.client.recordings.list(limit=limit)
        return [{"sid": r.sid, "duration": r.duration, "status": r.status, "url": f"https://api.twilio.com{r.uri.replace('.json', '.mp3')}"} for r in recordings]

    def create_access_token(self, identity: str):
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_SECRET,
            identity=identity
        )
        
        # Create a Voice Grant
        voice_grant = VoiceGrant(
            outgoing_application_sid=settings.TWILIO_APP_SID,
            incoming_allow=True, # Allow incoming calls to this client
        )
        token.add_grant(voice_grant)
        
        return token.to_jwt()

    def generate_twiml_for_browser_outbound(self, to_number: str):
        response = VoiceResponse()
        # Dial the number
        dial = Dial(caller_id=self.phone_number, record="record-from-answer")
        dial.number(to_number)
        response.append(dial)
        return str(response)

    def join_meeting(self, phone_number: str, pin: str, webhook_url: str):
        """
        Dial into a meeting (Google Meet, Teams, etc.) and record it.
        """
        call = self.client.calls.create(
            to=phone_number,
            from_=self.phone_number,
            url=f"{webhook_url}?pin={pin}",
            record=True
        )
        return call

    def generate_twiml_for_meeting(self, pin: str):
        """
        TwiML that waits briefly then sends DTMF tones (the PIN).
        """
        response = VoiceResponse()
        # Wait for the IVR to answer
        response.pause(length=3)
        # Send DTMF tones
        response.play(digits=pin)
        # Keep the call alive (record silence if no one talks)
        response.pause(length=14400)  # 4 hours max
        return str(response)

twilio_service = TwilioService()
