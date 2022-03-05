from pymongo import MongoClient

from constants import MONGO_URI


class Database:
    def __init__(self):
        client = MongoClient(MONGO_URI)["registros"]
        self.__collection = client["poemas"]
        self.records = self.__collection.count_documents({})

    def get_poem(self, id: int) -> object:
        return self.__collection.find_one({"_id": id})

    def get_poems(self, limit: int) -> list:
        return list(self.__collection.find().limit(limit))

    def create_poem(self, author: str, title: str, poem: list) -> bool:
        try:
            poems = self.get_poems(self.records)
            id = 1 if poems == [] else poems[-1].get("_id") + 1

            self.__collection.insert_one(
                {"_id": id, "author": author, "title": title, "poem": poem}
            )

            return True
        except:
            return False

    def update_poem(self, id: int, author: str, title: str, poem: list) -> bool:
        try:
            self.__collection.update_one(
                {"_id": id}, {"$set": {"author": author, "title": title, "poem": poem}}
            )

            return True
        except:
            return False

    def delete_poem(self, id: int) -> bool:
        try:
            self.__collection.delete_one({"_id": id})

            return True
        except:
            return False
