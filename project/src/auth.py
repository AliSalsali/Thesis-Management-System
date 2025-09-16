import hashlib
from src.database import load_data, save_data

def hash_password(password):
     
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password, hashed_password):
     
    return hash_password(plain_password) == hashed_password

def login(user_type, user_id, password):
     
    filename = f"{user_type}s.json"
    users = load_data(filename)
    for user in users:
        if user['user_id'] == user_id and verify_password(password, user['password_hash']):
            return user
    return None

def change_password_in_db(user_type, user_id, new_password):
     
    filename = f"{user_type}s.json"
    users = load_data(filename)
    user_found = False
    for user in users:
        if user['user_id'] == user_id:
            user['password_hash'] = hash_password(new_password)
            user_found = True
            break
    if user_found:
        save_data(filename, users)
        return True
    return False