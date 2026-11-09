"""TinyDB stores JSON-compatible account and player dictionaries."""
import hashlib
import hmac
import os
from pathlib import Path
from tinydb import TinyDB, Query

# A stable path prevents accidental different saves when launched elsewhere.
SAVE_PATH = Path(os.getenv("RPG_SAVE_PATH", str(Path(__file__).with_name("elden_ring_save.json"))))
Accounts = Query()

def open_db():
    return TinyDB(SAVE_PATH)

def find_account(username):
    with open_db() as db:
        return db.get(Accounts.username == username)

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200000).hex()

def create_account(username, password, player_data):
    salt = os.urandom(16).hex()
    with open_db() as db:
        if db.contains(Accounts.username == username):
            raise ValueError("That username already exists.")
        db.insert({"username": username, "salt": salt,
                   "password_hash": password_hash(password, salt), "player": player_data})

def verify_password(account, password):
    if "password_hash" in account:
        return hmac.compare_digest(account["password_hash"], password_hash(password, account["salt"]))
    # Allow the original classroom save and migrate it after a successful login.
    if account.get("password") != password: return False
    salt = os.urandom(16).hex()
    def migrate(doc):
        doc.pop("password", None)
        doc["salt"] = salt
        doc["password_hash"] = password_hash(password, salt)
    with open_db() as db: db.update(migrate, Accounts.username == account["username"])
    return True

def save_player(username, player_data):
    with open_db() as db:
        if not db.contains(Accounts.username == username):
            raise ValueError("Account was not found; progress cannot be saved.")
        db.update({"player": player_data}, Accounts.username == username)

def get_player(username):
    account = find_account(username)
    return account["player"] if account else None
