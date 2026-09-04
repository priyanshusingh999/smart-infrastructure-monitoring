from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(
    Config.MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
)
db = client[Config.MONGO_DBNAME]
users_collection = db["users"]
password_reset_collection = db["password_reset_tokens"]


_indexes_ready = False


def ensure_indexes():
    global _indexes_ready

    if _indexes_ready:
        return

    users_collection.create_index('email', unique=True)
    users_collection.create_index('username', unique=True)
    password_reset_collection.create_index('expires_at', expireAfterSeconds=0)
    _indexes_ready = True


def create_user(name, username, email, password):
    ensure_indexes()
    user = {"name": name, "username": username, "email": email, "password": password}
    result = users_collection.insert_one(user)
    return result.inserted_id

def get_user_by_email(email):
    return users_collection.find_one({"email": email})


def get_user_by_username(username):
    return users_collection.find_one({"username": username})

def get_user_by_id(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None
    return users_collection.find_one(
        {
            "_id": object_id
        }
    )


def get_all_users():
    return list(users_collection.find())


def update_user(user_id, name, username, email, password):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return False

    result = users_collection.update_one(
        {
            "_id": object_id
        },
        {
            "$set": {"name": name, "username": username, "email": email, "password": password}
        }
    )
    return result.modified_count > 0

def delete_user(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return False

    result = users_collection.delete_one(
        {
            "_id": object_id
        }
    )
    return result.deleted_count > 0