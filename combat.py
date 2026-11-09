import random
from colorama import Fore
from monster import EldenLord
from skill import SKILLS


def fight(player, monster):
    player.set("cooldowns", {})
    print(Fore.RED + "\nA " + monster.name + " blocks your path!")
    while monster.hp > 0 and player.get("hp") > 0:
        print("\nYour HP:", player.get("hp"), "/", player.get("max_hp"))
        print(monster.name + " HP:", monster.hp)
        print("1. Attack")
        print("2. Use a skill")
        print("3. Use an item")
        print("4. Try to run")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            damage = 10 + player.get("level") * 3
            if player.get("equipment") == "Knight's Greatsword":
                damage = damage + 15
            elif player.get("equipment") == "Moonveil Fragment":
                damage = damage + 12
            else:
                damage = damage + 5
            damage += player.get("attack_buff") or 0
            player.set("attack_buff", 0)
            monster.hp = monster.hp - damage
            print(Fore.GREEN + "You deal", damage, "damage.")
        elif choice == "2":
            skills = player.get("skills")
            for i, skill_name in enumerate(skills, 1):
                print(str(i) + ". " + skill_name)
            answer = input("Choose skill number: ").strip()
            try:
                index = int(answer) - 1
                if index < 0 or index >= len(skills):
                    raise IndexError
                skill_name = skills[index]
                skill = SKILLS[skill_name]
                cooldowns = player.get("cooldowns")
                if cooldowns.get(skill_name, 0) > 0:
                    print("That skill is cooling down for", cooldowns[skill_name], "more turn(s).")
                    continue
                else:
                    damage = skill.use(player, monster)
                    if damage > 0:
                        monster.hp = monster.hp - damage
                        print(Fore.MAGENTA + skill_name, "deals", damage, "damage!")
                    else:
                        print(Fore.GREEN + skill_name, "restores health!")
                    # Add one because cooldowns decrease at the end of this round.
                    cooldowns[skill_name] = skill.cooldown + 1
            except (ValueError, IndexError, KeyError):
                print("Choose a valid skill.")
                continue
        elif choice == "3":
            from inventory import use_item
            if not use_item(player):
                continue
        elif choice == "4":
            if isinstance(monster, EldenLord):
                print("You cannot flee from the final battle!")
            elif random.randint(1, 100) <= 45:
                print("You escaped.")
                return False
            else:
                print("You failed to escape!")
        else:
            print("Enter 1, 2, 3, or 4.")
            continue

        if monster.hp <= 0:
            break

        # Each completed combat round reduces existing cooldowns.
        for skill_name in player.get("cooldowns"):
            if player.get("cooldowns")[skill_name] > 0:
                player.get("cooldowns")[skill_name] = player.get("cooldowns")[skill_name] - 1

        if random.randint(1, 100) <= 20:
            damage = monster.special_move()
            print(Fore.RED + monster.name, "uses a special attack!")
        else:
            damage = monster.attack()
        player.take_damage(damage)
        print(Fore.RED + monster.name, "deals", damage, "damage.")

    if player.get("hp") <= 0:
        print(Fore.RED + "You have fallen. Rest, and try again.")
        player.set("lost", True)
        return False

    print(Fore.YELLOW + "You defeated", monster.name + "!")
    player.set("gold", player.get("gold") + monster.gold_drop)
    player.gain_xp(monster.xp_drop)
    print("You found", monster.gold_drop, "gold and", monster.xp_drop, "XP.")
    if monster.item_drop is not None:
        player.get("inventory").append(monster.item_drop)
        print("Item dropped:", monster.item_drop)
    if isinstance(monster, EldenLord):
        player.set("boss_defeated", True)
        player.set("won", True)
    return True
