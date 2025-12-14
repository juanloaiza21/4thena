
import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

# Load env from parent dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
NGROK_URL = "https://stemlike-marlyn-unflatterable.ngrok-free.dev"

if not ACCOUNT_SID or not AUTH_TOKEN:
    print("Error: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in .env")
    sys.exit(1)

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def create_api_key():
    print("Creating new API Key...")
    new_key = client.new_keys.create(friendly_name="Apollo API Key")
    print(f"API Key Created: {new_key.sid}")
    return new_key.sid, new_key.secret

def create_twiml_app(ngrok_url):
    print("Creating/Updating TwiML App...")
    voice_url = f"{ngrok_url}/calls/outgoing-browser"
    
    # Check if we already have one
    apps = client.applications.list(friendly_name="Apollo Softphone")
    if apps:
        app = apps[0]
        print(f"Found existing app {app.sid}, updating URL to {voice_url}")
        app = app.update(voice_url=voice_url)
    else:
        app = client.applications.create(
            friendly_name="Apollo Softphone",
            voice_url=voice_url
        )
        print(f"Created new app {app.sid}")
        
    return app.sid

def update_env_file(api_key, api_secret, app_sid):
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    with open(env_path, "a") as f:
        f.write(f"\nTWILIO_API_KEY={api_key}")
        f.write(f"\nTWILIO_API_SECRET={api_secret}")
        f.write(f"\nTWILIO_APP_SID={app_sid}")
        f.write(f"\nNGROK_URL={NGROK_URL}")
    print("Updated .env file with new credentials.")

if __name__ == "__main__":
    try:
        key_sid, key_secret = create_api_key()
        app_sid = create_twiml_app(NGROK_URL)
        update_env_file(key_sid, key_secret, app_sid)
        print("\n✅ Setup Complete! Please restart your application.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
