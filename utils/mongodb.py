import os

from pymongo import MongoClient
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)


class MongoDB:
    def __init__(self):
        """Initializes a MongoDB client and database."""
        self.db = None
        self.client = MongoClient(os.getenv("MONGO_URI"))

    def resolve_db(self, db_name: str = None):
        if os.getenv("LOCAL") == "True":
            self.db = self.client[os.getenv("DB_NAME")]
        else:
            self.db = self.client[db_name or os.getenv("DB_NAME")]

    def find_one(self, collection, query, projection=None) -> dict:
        """Returns a single document from the collection."""
        return self.db[collection].find_one(query, (projection or {"_id": 0}))

    def find(self, collection, query, projection=None) -> list:
        """Returns a list of documents from the collection."""
        return list(self.db[collection].find(query, (projection or {"_id": 0})))

    def insert_one(self, collection, document) -> InsertOneResult:
        """Inserts a single document into the collection."""
        return self.db[collection].insert_one(document)

    def insert_many(self, collection, documents) -> InsertManyResult:
        """Inserts multiple documents into the collection."""
        return self.db[collection].insert_many(documents)

    def update_one(self, collection, query, update) -> UpdateResult:
        """Updates a single document in the collection."""
        return self.db[collection].find_one_and_update(query, update, upsert=True)

    def update_many(self, collection, query, update) -> UpdateResult:
        """Updates multiple documents in the collection."""
        return self.db[collection].update_many(query, update, upsert=True)

    def delete_one(self, collection, query, projection=None) -> DeleteResult:
        """Deletes a single document from the collection."""
        return self.db[collection].find_one_and_delete(query, projection)

    def delete_many(self, collection, query, projection=None) -> DeleteResult:
        """Deletes multiple documents from the collection."""
        return self.db[collection].delete_many(query, projection)
