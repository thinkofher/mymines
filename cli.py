import sys
import click
from mine import visualize_field, MineGameField


def x_y_input():
    x = input(">>> Enter x: ")
    y = input(">>> Enter y: ")
    return (int(x), int(y))


_INFO = """
Welcome in Mine Sweeper game!
This application was completly written
in Python by Beniamin Dudek @2019.
I hope you will enjoy it!

If you need help type h in game prompt!
"""

_HELP = """
    c == Reaveals given cell
    a == Reaveals everything around given cell
         as long it is not flagged.
    f == Flags given cell
    h == Help
    q == Quit
"""


@click.command()
@click.option('-w', '--width', default=8, help='Width of minefield.')
@click.option('-h', '--height', default=8, help='Height of minefield')
@click.option('-n', '--n_of_bombs', default=10,
              help='Number of randomly spawned bombs in minefield')
def main(width, height, n_of_bombs):
    """
    CLI implementation of Minesweeper game
    """
    game = MineGameField(
        width, height, n_of_bombs)
    print(_INFO)

    # uncomment if you want to debug
    # visualize_field(game, hidden=False)

    print()
    visualize_field(game)
    print()

    while True:
        print("\nWhat do you want to do? (c, a, f, h, q): ")
        action = input(">>> ").lower()

        try:
            if action == 'c':
                cords = x_y_input()
                game.player_check(cords)
            elif action == 'a':
                cords = x_y_input()
                game.player_check_arround(cords)
            elif action == 'f':
                cords = x_y_input()
                game.toggle_flag(cords)
            elif action == 'h':
                print(_HELP)
            else:
                break
        except (KeyError, ValueError):
            print('>>> Bad input. Try Again. <<<')

        if game.is_won():
            print()
            visualize_field(game, hidden=False)
            print()
            print(">>> You won. Congratulations!")
            sys.exit(0)
        if game.is_loss():
            print()
            visualize_field(game, hidden=False)
            print()
            print(">>> You lost. You can try again!")
            sys.exit(0)

        print()
        visualize_field(game)


if __name__ == '__main__':
    main()
