from passlib.context import CryptContext
from uuid import uuid4
from db import users_collection
from jwt_utils import create_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def register_user(username: str, password: str):
    if users_collection.find_one({"username": username}):
        return {"error": "Usuario ya existe"}

    user_id = str(uuid4())
    hashed_password = hash_password(password)
    users_collection.insert_one({
        "_id": user_id,
        "username": username,
        "password": hashed_password
    })
    return {"user_id": user_id}

def login_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "Usuario no encontrado"}

    if not verify_password(password, user["password"]):
        return {"error": "Contraseña incorrecta"}
    
    token = create_token({"user_id": user["_id"], "username": user["username"]})

    return {"token": token}
