import asyncio
import colorama
from colorama import Fore
from dotenv import load_dotenv
import os

from manager.load_config import CONFIG

from service.nats_consumer import NATSConsumer

load_dotenv()

colorama.init(autoreset=True)

async def main():
    print(f"{Fore.BLUE}Starting Hera API NATS Consumer...")
    
    if CONFIG is None:
        print(f"{Fore.RED}Error: 'config.yaml' is empty or invalid.")
        return

    if 'nats' not in CONFIG:
        print(f"{Fore.RED}Error: 'nats' section missing in config.yaml")
        return

    nats_config = CONFIG["nats"]
    server = nats_config.get("server", "nats://nats-mq:4222")
    consumer_subject = nats_config.get("consumer_subject", "hera.predict.id")

    consumer = NATSConsumer(server, consumer_subject)

    await consumer.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Shutting down...")
