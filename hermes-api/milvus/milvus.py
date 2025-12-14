from typing import List
from colorama import Fore
from pymilvus import MilvusClient

from .schema import IDENTIFYING_MSG_SCHEMA, RAG_SCHEMA

class Milvus:
    def __init__(self, uri: str, identify_collection: str, rag_collection: str):
        self.client: MilvusClient | None = None
        self.uri = uri
        self.identify_collection = identify_collection
        self.rag_collection = rag_collection

    async def connect(self) -> None:
        print(f"{Fore.GREEN}Attempting milvus connection on uri {self.uri}")

        try:
            self.client = MilvusClient(uri=self.uri)
            _ = self.client.list_collections()
        except Exception as e:
            print(f"{Fore.RED}Couldn't establish connection to milvus")
            raise e

        if not self.client.has_collection(self.identify_collection):
            print(f"{Fore.BLUE}Milvus collection {self.identify_collection} doesn't exist, creaturing nowkljA")
            
            self.client.create_collection(
                collection_name=self.identify_collection,
                schema=IDENTIFYING_MSG_SCHEMA,
                metric_type="COSINE"
            )

            print(f"{Fore.GREEN}Milvus collection {self.identify_collection} created successfully")

            index_params = self.client.prepare_index_params(
                field_name="vector",
                index_type="IVF_SQ8",
                metric_type="COSINE",
                params={"nlist":1024}
            )
            self.client.create_index(
                collection_name=self.identify_collection,
                index_params=index_params
            )
        else:
            print(f"{Fore.GREEN}Milvus collection {self.identify_collection} already exists")

        self.client.load_collection(
            collection_name=self.identify_collection
        )

    async def buildMerchantCollection(self, merchant_id: str):
        if self.client is None:
            print(f"{Fore.RED}Please run connect() first")
            raise Exception("Please run connect() first")

        merchant_collection = self.rag_collection+f"_{merchant_id}"

        if not self.client.has_collection(merchant_collection):
            print(f"{Fore.BLUE}Milvus collection {merchant_collection} doesn't exist, creaturing nowkljA")
            
            self.client.create_collection(
                collection_name=merchant_collection,
                schema=RAG_SCHEMA,
                metric_type="COSINE"
            )

            print(f"{Fore.GREEN}Milvus collection {merchant_collection} created successfully")

            index_params = self.client.prepare_index_params(
                field_name="vector",
                index_type="IVF_SQ8",
                metric_type="COSINE",
                params={"nlist":1024}
            )
            self.client.create_index(
                collection_name=merchant_collection,
                index_params=index_params
            )
        else:
            print(f"{Fore.GREEN}Milvus collection {merchant_collection} already exists")

        state = self.client.get_load_state(collection_name=merchant_collection)
        if state["state"] != "Loaded":
            self.client.load_collection(
                collection_name=merchant_collection
            )

        return merchant_collection


    async def insertIdentify(self, vector: List[float], merchant_id: str, msg_id: str) -> None:
        if self.client is None:
            print(f"{Fore.RED}Please run connect() first")
            raise Exception("Please run connect() first")

        try:
            print(f"{Fore.BLUE}Insering into milvus collection {self.identify_collection}")
            self.client.insert(
                collection_name=self.identify_collection,
                data=[
                    {
                        "merchant_id": merchant_id,
                        "msg_id": msg_id,
                        "vector": vector
                    }
                ]
            )
        except Exception as e:
            print(f"{Fore.RED}Inserting into Milvus collection {self.identify_collection} FAILED")
            print(e)
            return

    async def insertRag(self, vector: List[float], merchant_id: str, msg_id: str) -> None:
        if self.client is None:
            print(f"{Fore.RED}Please run connect() first")
            raise Exception("Please run connect() first")

        merchant_collection = await self.buildMerchantCollection(merchant_id)

        try:
            print(f"{Fore.BLUE}Insering into milvus collection {merchant_collection}")
            self.client.insert(
                collection_name=merchant_collection,
                data=[
                    {
                        "merchant_id": merchant_id,
                        "msg_id": msg_id,
                        "vector": vector
                    }
                ]
            )
        except Exception as e:
            print(f"{Fore.RED}Inserting into Milvus collection {merchant_collection} FAILED")
            print(e)
            return
