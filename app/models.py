from datetime import datetime
import string
import random
from bson import ObjectId

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class URL:
    def __init__(self, db):
        self.collection = db.urls

    def create(self, original_url):
        short_code = generate_short_code()
        while self.collection.find_one({"shortCode": short_code}):
            short_code = generate_short_code()
        
        url_data = {
            "originalUrl": original_url,
            "shortCode": short_code,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "accessCount": 0
        }
        result = self.collection.insert_one(url_data)
        return self.collection.find_one({"_id": result.inserted_id})

    def find_by_short_code(self, short_code):
        return self.collection.find_one({"shortCode": short_code})

    def update_url(self, short_code, new_url):
        return self.collection.update_one(
            {"shortCode": short_code},
            {"$set": {
                "originalUrl": new_url,
                "updatedAt": datetime.utcnow()
            }}
        )

    def delete_url(self, short_code):
        return self.collection.delete_one({"shortCode": short_code})

    def increment_access_count(self, short_code):
        return self.collection.update_one(
        {"shortCode": short_code},
        {"$inc": {"accessCount": 1}}  # Verify field name matches your documents
    )