import sys
import pygame
from asteroid import Asteroid
from asteroidField import AsteroidField
from player import Player
from shot import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event

def main():
    print("Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # instances
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0

    while True:
      # logs found in game_state.jsonl
      log_state()

      # makes game window close button work
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return

      # rotate player with keypress
      for updatable_item in updatable:
        updatable_item.update(dt)

      # check for player to astroid collisions
      for asteroid in asteroids:
        if player.collides_with(asteroid):
          log_event("player_hit")
          print("Game over!")
          sys.exit()
        for shot in shots:
          if shot.collides_with(asteroid):
            log_event("asteroid_shot")
            asteroid.split()
            shot.kill()

      # background color
      screen.fill("black")

      # render screen
      for drawable_item in drawable:
        drawable_item.draw(screen)

      # refresh the screen
      pygame.display.flip()

      # limit framerate to 60 FPS
      time_passed = clock.tick(60)
      dt = time_passed / 1000
      # print(f"time passed: {dt}")


      # if condition_1:
      #   break


if __name__ == "__main__":
    main()
