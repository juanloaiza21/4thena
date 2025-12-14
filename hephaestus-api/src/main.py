import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.message.message_controller import MessageController
from src.core.database.session import connect_to_mongo, close_mongo_connection
from src.core.nats import NatsConnection

sys.path.append(os.path.join(os.getcwd(), "./src"))

# NATS connection for publishing only
nats = NatsConnection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    print("✅ Connected to MongoDB")

    await nats.get_connection()
    print("✅ Connected to NATS")

    # Make NATS available to the app
    app.state.nats = nats

    yield

    # Shutdown
    await nats.close()
    await close_mongo_connection()
    print("👋 All connections closed")


app = FastAPI(
    title="Chronos API",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(MessageController.router())
