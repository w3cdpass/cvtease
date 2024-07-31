import os
import time
import random
import sys
import select

def play_game():
    width, height = 40, 20
    spaceship = [' ^ ', '/|\\', '/ \\']
    asteroid = ['***', '***', '***']
    score = 0
    lives = 3
    spaceship_x, spaceship_y = width // 2 - 1, height - 3

    asteroids = [(random.randint(0, width - 3), random.randint(0, height - 6)) for _ in range(5)]

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(screen):
        clear_screen()
        for line in screen:
            print(''.join(line))
        print(f'Score: {score}  Lives: {lives}')
        print('Controls: A - Left, D - Right, Q - Quit')

    def move_asteroids():
        nonlocal score, lives
        new_asteroids = []
        for x, y in asteroids:
            if y < height - 3:
                new_asteroids.append((x, y + 1))
            else:
                score += 1
                new_asteroids.append((random.randint(0, width - 3), 0))
            # Check for collision
            if any(
                spaceship_x <= x + j < spaceship_x + 3 and spaceship_y <= y + i < spaceship_y + 3
                for i in range(3) for j in range(3)
            ):
                lives -= 1
                new_asteroids[-1] = (random.randint(0, width - 3), 0)
                if lives == 0:
                    print("Game Over!")
                    sys.exit()
        return new_asteroids

    def getch():
        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')
        else:
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

    def create_screen():
        return [[' ' for _ in range(width)] for _ in range(height)]

    def update_screen(screen):
        # Draw asteroids
        for x, y in asteroids:
            for i in range(3):
                for j in range(3):
                    if 0 <= y + i < height and 0 <= x + j < width:
                        screen[y + i][x + j] = '\033[91m' + asteroid[i][j] + '\033[0m'  # Red color for asteroids

        # Draw spaceship
        for i in range(3):
            for j in range(3):
                if 0 <= spaceship_y + i < height and 0 <= spaceship_x + j < width:
                    screen[spaceship_y + i][spaceship_x + j] = spaceship[i][j]

    screen = create_screen()
    clear_screen()

    while True:
        new_screen = create_screen()
        update_screen(new_screen)

        if screen != new_screen:
            draw(new_screen)
            screen = new_screen

        asteroids = move_asteroids()
        time.sleep(0.1)
        
        key = getch()
        if key:
            if key == 'q':
                break
            elif key == 'a' and spaceship_x > 0:
                spaceship_x -= 1
            elif key == 'd' and spaceship_x < width - 3:
                spaceship_x += 1

if __name__ == '__main__':
    play_game()
