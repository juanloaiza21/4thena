from typing import List
from pymongo import MongoClient
import os
from colorama import Fore
from manager.load_config import CONFIG

client = None

def get_db():
    global client
    if client is not None:
        return client

    print(f"{Fore.BLUE}Attempting connection to mongo")
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "athena_db")
    client = MongoClient(mongo_uri)
    print(f"{Fore.GREEN}Mongo connection established")
    return client[db_name]

def getQueryMsgs(msg_ids: List[str]):
    db = get_db()

    print(f"{Fore.BLUE}Querying messages table")
    messages_col = db["messages"]
    messages_cursor = messages_col.find({"_id": {"$in": msg_ids}})

    full_msgs_txt = []
    for doc in messages_cursor:
        full_msgs_txt.append(doc["txt"])

    print(f"{Fore.BLUE}Found a total of {len(full_msgs_txt)}")
    
    return full_msgs_txt
        

def getContractMessages(merchant_id: str):
    db = get_db()
    
    collection_name = f"merchant_{merchant_id}"
    
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"{Fore.GREEN}Created collection: {collection_name}")
    
    merchant_col = db[collection_name]
    
    cursor = merchant_col.find({}, {"msg_id": 1, "_id": 0})
    msg_ids = [doc['msg_id'] for doc in cursor if 'msg_id' in doc]
    
    messages_col = db["messages"]
    
    results = []
    if msg_ids:
        messages_cursor = messages_col.find({"msg_id": {"$in": msg_ids}})
        results = list(messages_cursor)
        
    print("\n--- CONTRACT MESSAGES ---")
    for res in results:
        print(res)
    print("-------------------------\n")
    
    return results
