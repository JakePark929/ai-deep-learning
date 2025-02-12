import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_INITDB_HOST = os.getenv('MONGO_INITDB_HOST')
MONGO_INITDB_PORT = int(os.getenv('MONGO_INITDB_PORT'))
MONGO_INITDB_ROOT_USERNAME  = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD  = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

client = MongoClient(
    host=MONGO_INITDB_HOST, 
    port=MONGO_INITDB_PORT,
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
    authSource='admin'
)

db = client['baemin_recommendation']
collection = db['recommendation']

print(client.server_info())

# test_data = {"name": "test", "value": 123}
# collection.insert_one(test_data)
# print("Inserted: ", test_data)

documents = list(collection.find({}))
print(documents)