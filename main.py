import pygame
from enum import Enum
import os

from game import Game, Reset
from button import Button
from title import Title

os.chdir(f"{os.getcwd()}/assets")

def entry_point():
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    CHANNEL = pygame.mixer.Channel(1)

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gorillas")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('dejavusans', 30)

    class Scene(Enum):
        GAME = 0,
        RESET = 1,
        TITLE = 2
    
    scenes = {
        Scene.GAME:  Game(SCREEN, CHANNEL),
        Scene.RESET: Reset(SCREEN, CHANNEL, font),
        Scene.TITLE: Title(SCREEN, CHANNEL, font)
    }

    Button.load_sounds()

    active_scene = Scene.TITLE
    run = True
    dt = 0.0001

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        scenes[active_scene].update(dt)

        if scenes[Scene.TITLE].quit:
            run = False
        
        if scenes[Scene.TITLE].play:
            scenes[Scene.TITLE].play = False
            scenes[Scene.GAME].setup_game()
            active_scene = Scene.GAME

        if scenes[Scene.GAME].game_over >= 0:
            winner = scenes[Scene.GAME].game_over
            scenes[Scene.RESET].winner = winner
            scenes[Scene.GAME].game_over = -1
            active_scene = Scene.RESET
        
        if scenes[Scene.RESET].click:
            scenes[Scene.RESET].click = False
            scenes[Scene.GAME].setup_game()
            active_scene = Scene.GAME
        elif scenes[Scene.RESET].menu:
            scenes[Scene.RESET].menu = False
            active_scene = Scene.TITLE
        
        scenes[active_scene].draw()

        pygame.display.update()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    entry_point()
    pygame.quit()
