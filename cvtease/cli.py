import click
from .game import play_game
from .recoface import open_camera
from PySide6.QtWidgets import QApplication
from .gui import FaceDetectionApp
import sys
@click.command()
@click.option('--gui', is_flag=True, help='Launch the GUI application.')
@click.option('--game', is_flag=True, help='Play the space shooter game.')
@click.option('-a', '--access-camera', is_flag=True, help='Open the camera and perform face detection.')
@click.option('-fk', '--facial-keypoints', is_flag=True, help='Activate facial keypoints detection.')
def main(gui, game, access_camera, facial_keypoints):
    if gui:
        app = QApplication(sys.argv)
        window = FaceDetectionApp()
        window.show()
        sys.exit(app.exec())
    elif game:
        play_game()
    elif access_camera:
        open_camera(facial_keypoints)
    else:
        click.echo(click.get_current_context().get_help())
        click.echo("This tool is under development, so be patient.")

if __name__ == '__main__':
    main()