import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print("Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    while True:
      # logs found in game_state.jsonl
      log_state()

      # makes game window close button work
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return

      # background color
      screen.fill("black")

      # refresh the screen
      pygame.display.flip()

      # if condition_1:
      #   break


if __name__ == "__main__":
    main()
