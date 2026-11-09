from colorama import Fore
from database import find_account, create_account, verify_password
from getpass import getpass


def new_player_data(name):
    return {
        "name": name,
        "hp": 100,
        "max_hp": 100,
        "xp": 0,
        "level": 1,
        "gold": 25,
        "inventory": ["Crimson Flask", "Crimson Flask", "Rusty Sword"],
        "skills": ["Heavy Strike"],
        "cooldowns": {},
        "map_name": "Limgrave",
        "x": 1,
        "y": 1,
        "main_quest": 0,
        "side_quests": [],
        "completed_side_quests": [],
        "equipment": "Rusty Sword",
        "boss_defeated": False,
        "won": False,
        "lost": False
    }


def register_or_login():
    while True:
        print(Fore.CYAN + "\n1. Log in\n2. Register\n3. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = getpass("Password: ")
            account = find_account(username)
            if account is not None and verify_password(account, password):
                print(Fore.GREEN + "Welcome back, Tarnished.")
                return account["player"] | {"username": username}
            print(Fore.RED + "Login failed. Check your username and password.")

        elif choice == "2":
            username = input("Choose a username: ").strip()
            if len(username) == 0:
                print(Fore.RED + "Username cannot be empty.")
            elif find_account(username) is not None:
                print(Fore.RED + "That username already exists.")
            else:
                password = getpass("Choose a password: ")
                if len(password) == 0:
                    print(Fore.RED + "Password cannot be empty.")
                else:
                    name = input("Character name: ").strip()
                    if len(name) == 0:
                        name = "Tarnished"
                    data = new_player_data(name)
                    create_account(username, password, data)
                    print(Fore.GREEN + "Account created. You may now log in.")
        elif choice == "3":
            return None
        else:
            print(Fore.RED + "Enter 1, 2, or 3.")
