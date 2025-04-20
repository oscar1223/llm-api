from langchain_core.memory import BaseMemory
from db import db
from bson import ObjectId

memory_collection = db["memories"]

class MongoMemory(BaseMemory):
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def memory_variables(self):
        return ["chat_history"]

    def load_memory_variables(self, inputs):
        memory = memory_collection.find_one({"user_id": self.user_id})
        return {"chat_history": memory["chat_history"] if memory else []}

    def save_context(self, inputs, outputs):
        new_entry = {
            "input": inputs,
            "output": outputs
        }
        memory_collection.update_one(
            {"user_id": self.user_id},
            {"$push": {"chat_history": new_entry}},
            upsert=True
        )

    def clear(self):
        memory_collection.delete_one({"user_id": self.user_id})
