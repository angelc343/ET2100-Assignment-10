from colorama import init, Fore, Style
from auth import register_or_login
from game import Game

init(autoreset=True)


def main():
    print(Fore.YELLOW + Style.BRIGHT + """
========================================================
          ELDEN RING: SHATTERED GRACE
========================================================
The Elden Ring has been shattered. The Lands Between lie
in ruin, and the throne waits for a Tarnished brave enough
to claim it. Find the Great Runes, aid the lost, and face
the Elden Lord who guards the final path.
========================================================
""")
    while True:
        player_data = register_or_login()
        if player_data is None:
            print(Fore.CYAN + "Farewell, Tarnished.")
            break

        game = Game(player_data)
        game.run()

        answer = input("\nReturn to the title screen? (yes/no): ").strip().lower()
        if answer != "yes":
            print(Fore.YELLOW + "May grace guide your path.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nMay grace guide your path.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load or save game data:", error)
        print("Keep a backup of elden_ring_save.json and check its format and permissions.")
        print("The game has stopped; your existing save was not intentionally reset.")
