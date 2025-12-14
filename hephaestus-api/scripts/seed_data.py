import asyncio
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.join(os.getcwd(), "."))

from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

async def seed_data():
    print(f"🔌 Conectando a MongoDB en: {settings.MONGO_URI}...")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_NAME]
    collection = db["messages"]

    test_messages = [
        {
            "source": "whatsapp",
            "content": {
                "text": "Hola, necesito ayuda con mi pedido #12345",
                "phone": "+573001234567",
                "timestamp": "2024-05-20T10:00:00Z"
            },
            "ratified": False,
            "merchantId": "test_merchant"
        },
        {
            "source": "email",
            "content": {
                "subject": "Reclamo de facturación",
                "body": "No reconozco el cargo de $50 USD en mi tarjeta.",
                "sender": "juan@example.com"
            },
            "ratified": False,
            "merchantId": "test_merchant"
        },
        {
            "source": "call",
            "content": {
                "duration": 120,
                "recording_url": "http://example.com/rec/987.mp3",
                "transcript": "Buenas tardes, quiero cancelar mi suscripción."
            },
            "ratified": False,
            "merchantId": "other_merchant"
        },
        {
             "source": "linkedin",
             "content": {
                 "profile_url": "https://linkedin.com/in/usuario",
                 "message": "Me interesa saber más sobre sus servicios B2B."
             },
             "ratified": False,
             "merchantId": "test_merchant"
        }
    ]

    print("🌱 Insertando datos de prueba...")
    result = await collection.insert_many(test_messages)
    
    print(f"✅ Se insertaron {len(result.inserted_ids)} mensajes de prueba.")
    print("\n📋 IDs generados (COPIA ESTOS PARA PROBAR /ratify):")
    print("---------------------------------------------------")
    for msg_id in result.inserted_ids:
        print(f'"{msg_id}"')
    print("---------------------------------------------------")

if __name__ == "__main__":
    try:
        asyncio.run(seed_data())
    except Exception as e:
        print(f"❌ Error: {e}")
