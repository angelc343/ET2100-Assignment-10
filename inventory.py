from colorama import Fore
from item import ITEMS


def show_inventory(player):
    inventory = player.get("inventory")
    print(Fore.YELLOW + "\n--- Inventory ---")
    if len(inventory) == 0:
        print("Your inventory is empty.")
    else:
        for number, item_name in enumerate(inventory, 1):
            print(str(number) + ". " + item_name)


def use_item(player):
    inventory = player.get("inventory")
    show_inventory(player)
    if len(inventory) == 0:
        return False

    answer = input("Enter item number to use, or press Enter to cancel: ").strip()
    if answer == "":
        return False
    try:
        number = int(answer)
    except ValueError:
        print(Fore.RED + "Please enter a number.")
        return False

    if number < 1 or number > len(inventory):
        print(Fore.RED + "That item number is not in your inventory.")
        return False

    item_name = inventory[number - 1]
    item = ITEMS.get(item_name)
    if item is None:
        print("You cannot use that item.")
        return False

    if item.item_type == "heal":
        if player.get("hp") == player.get("max_hp"):
            print("Your HP is already full.")
        else:
            player.heal(item.power)
            inventory.pop(number - 1)
            print(Fore.GREEN + "You used", item_name, "and restored", item.power, "HP.")
            return True
    elif item.item_type == "gold":
        player.set("gold", player.get("gold") + item.power)
        inventory.pop(number - 1)
        print("You gained", item.power, "gold.")
        return True
    elif item.item_type == "xp":
        player.gain_xp(item.power)
        inventory.pop(number - 1)
        print("You gained", item.power, "XP.")
        return True
    elif item.item_type == "weapon":
        player.set("equipment", item_name)
        print("Equipped", item_name)
        return True
    elif item.item_type == "buff":
        player.set("attack_buff", item.power)
        inventory.pop(number - 1)
        print("Your next normal attack gains", item.power, "damage.")
        return True
    else:
        print("That item cannot be used from this menu.")
    return False
