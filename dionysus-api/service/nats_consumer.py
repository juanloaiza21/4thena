import asyncio
import nats
from nats.errors import NoServersError
from colorama import Fore
import json

import traceback


from mongo import mongo

class NATSConsumer:
    def __init__(
        self,
        server: str,
        subject: str
    ):
        self.server = server
        self.subject = subject
        self.nc = None

        self.queue: asyncio.Queue = asyncio.Queue()

    async def connect(self):
        print(f"{Fore.GREEN}Attempting NATS connection")
        try:
            self.nc = await nats.connect(self.server)
            print(f"{Fore.GREEN}Connected to NATS servers: {self.server}")
        except NoServersError:
            print(f"{Fore.RED}Could not connect to any NATS server.")
            return

    async def message_handler(self, msg):
        print(f"{Fore.GREEN} incoming message {msg}")
        await self.queue.put(msg)

    async def process_message(self, msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"{Fore.CYAN}[{subject}] {data}")

        json_data = json.loads(data)

        mongo.updateMessageMerchantId(json_data["merchant_id"], json_data["msg_id"])
        

    async def worker(self):
        while True:
            msg = await self.queue.get()
            try:
                await self.process_message(msg)
            except Exception as e:
                print(f"{Fore.RED}Error processing message: {e}")
                print(e.__traceback__)
                traceback.print_stack()
            finally:
                self.queue.task_done()

    async def subscribe(self):
        if not self.nc:
            print(f"{Fore.YELLOW}Not connected to NATS. Cannot subscribe.")
            return

        await self.nc.subscribe(self.subject, cb=self.message_handler)
        print(f"{Fore.GREEN}Subscribed to: {self.subject}")

    async def run(self):
        await self.connect()
        await self.subscribe()

        asyncio.create_task(self.worker())

        while True:
            await asyncio.sleep(1)
