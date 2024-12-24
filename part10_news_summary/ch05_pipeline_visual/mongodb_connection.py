import os
import datetime

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

print(client.list_database_names())

db = client['test']
collection = db['NewsText']

print(db)
print(collection)

# 데이터 삽입
# item = {
#     "title": "제이크소프트 주가 일시 상승.",
#     "text": "제이크소프트의 주가가 일시적으로 상승했다. 장중 최고치는...",
#     "date": datetime.datetime.now()
# }

# insert_id = collection.insert_one(item).inserted_id
# print(insert_id)

# 데이터 조회
print(collection.find_one())