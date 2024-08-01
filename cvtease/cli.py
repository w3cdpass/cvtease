
### cli.py


import click
from .game import play_game

@click.command()
@click.option('--game', is_flag=True, help='Play the space shooter game.')
def main(game):
    if game:
        play_game()
    else:
        print("This tool is under development, so be patient.")

if __name__ == '__main__':
    main()
