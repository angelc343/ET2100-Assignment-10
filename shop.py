from colorama import Fore
from item import ITEMS


SHOP_ITEMS = ["Crimson Flask", "Smithing Stone", "Fire Grease", "Knight's Greatsword", "Moonveil Fragment"]


def visit_shop(player):
    while True:
        print(Fore.YELLOW + "\n--- Merchant Kale's Shop ---")
        print("Your gold:", player.get("gold"))
        for number, name in enumerate(SHOP_ITEMS, 1):
            item = ITEMS[name]
            print(str(number) + ". " + name + " - " + str(item.price) + " gold: " + item.description)
        print("0. Leave shop")
        answer = input("Buy which item? ").strip()
        if answer == "0":
            return
        try:
            index = int(answer) - 1
            if index < 0 or index >= len(SHOP_ITEMS):
                raise IndexError
            name = SHOP_ITEMS[index]
        except (ValueError, IndexError):
            print(Fore.RED + "Choose a listed item number.")
            continue

        item = ITEMS[name]
        if player.get("gold") < item.price:
            print(Fore.RED + "Not enough gold.")
        else:
            player.set("gold", player.get("gold") - item.price)
            if item.item_type == "weapon":
                player.get("inventory").append(name)
                player.set("equipment", name)
                print(Fore.GREEN + "Equipped", name + ".")
            else:
                player.get("inventory").append(name)
                print(Fore.GREEN + "Bought", name + ".")
