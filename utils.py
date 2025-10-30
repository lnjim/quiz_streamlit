import bcrypt
import re

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def validate_password(password):
    """Return True if password meets all criteria"""
    return all([
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(r"\d", password),
        re.search(r"[!@#$%^&*]", password),
        len(password) >= 8
    ])
