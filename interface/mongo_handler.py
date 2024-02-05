from pymongo.mongo_client import MongoClient
from pymongo import IndexModel, ASCENDING
from pymongo.errors import OperationFailure, WriteError

from racehorse.entity.config import MongoDBConfig


class MongoDBHandler:
    def __init__(self):
        uri = f"mongodb+srv://{MongoDBConfig.get('USERNAME')}:{MongoDBConfig.get('PASSWORD')}@{MongoDBConfig.get('DATABASE')}.pf3ahzc.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        self.client = MongoClient(uri)

        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def create_ttl_index(self, collection_name, index_field):
        # TTL 인덱스 생성
        try:
            # 인덱스 모델 설정
            index_model = IndexModel([(index_field, ASCENDING)], expireAfterSeconds=1 * 24 * 60 * 60)

            # 컬렉션에 TTL 인덱스 생성
            collection = self.client[MongoDBConfig.get('DATABASE')][collection_name]
            collection.create_indexes([index_model])

            print(f"TTL index created on {index_field} and trade_timestamp for {collection_name} collection.")
        except OperationFailure as e:
            print(f"Error creating TTL index: {e}")

    def insert_document(self, collection_name, document):
        # 문서 삽입 코드
        collection = self.client[MongoDBConfig.get('DATABASE')][collection_name]
        try:
            result = collection.insert_one(document)
            print(f"Document inserted with ID: {result.inserted_id}")
        except WriteError as e:
            print(f"Insert failed: {e}")
            pass

    def find_documents(self, collection_name, query, projection={}):
        # 문서 검색 코드
        collection = self.client[MongoDBConfig.get('DATABASE')][collection_name]
        cursor = collection.find(query, projection)
        documents = list(cursor)
        return documents

    def update_document(self, collection_name, query, update_data):
        # 문서 업데이트 코드
        collection = self.client[MongoDBConfig.get('DATABASE')][collection_name]
        result = collection.update_many(query, {"$set": update_data})
        print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

    def delete_document(self, collection_name, query):
        # 문서 삭제 코드
        collection = self.client[MongoDBConfig.get('DATABASE')][collection_name]
        result = collection.delete_many(query)
        print(f"Deleted {result.deleted_count} documents")

# MongoDBHandler().create_ttl_index("rise_top_5", "trade_timestamp")

# collection_name = "rise_top_5"
# index_field = "trade_timestamp"
# collection = MongoDBHandler().client[MongoDBConfig.get('DATABASE')][collection_name]
#
# # 기존 TTL 인덱스 삭제
# collection.drop_index("trade_timestamp_1")
#
# # 새로운 TTL 인덱스 생성
# collection.create_index([(index_field, 1)], expireAfterSeconds=2.3 * 24 * 60 * 60)
