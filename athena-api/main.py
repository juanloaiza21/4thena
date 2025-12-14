from dotenv import load_dotenv

load_dotenv()

from typing import Dict

from manager.load_config import CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import query, contract

import colorama

colorama.init(autoreset=True)

app = FastAPI() # DEVELOPMENT

origins = ["*"]  # CHANGE IN PROD ENV

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create persistence connection pools
@app.on_event("startup")
def create_persistence_connection_pools() -> None:
    pass


@app.on_event("shutdown")
def close_mysql_connection_pool() -> None:
    pass

# Add routers
app.include_router(query.router)
app.include_router(contract.router)
