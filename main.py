import pygame
from sys import exit
# User-generated
import screens


# Basic Arguments
screen_dimensions = (500, 600)
app_title = "Tic-Tac-Toe"
# Pygame Class Initialization
pygame.init()
screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption(app_title)
clock = pygame.time.Clock()
# Screen Class Initialization
Main = screens.MainScreen(screen, screen_dimensions)
Selection = screens.CharacterSelectionScreen(screen, screen_dimensions)
Game = screens.GameScreen(screen, screen_dimensions)
Result = screens.ResultScreen(screen, screen_dimensions)
status = "HOME"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or status == "QUIT":
            pygame.quit()
            exit()
    # Critical Code
    if status == "HOME":
        forward, backward = Main.populate_content()
        status = forward if forward is not None else status
        status = backward if backward is not None else status
    elif status == "SELECT":
        forward, backward, player_1_col, player_2_col = Selection.populate_content()
        if backward is not None:
            status = backward
            Selection.reset_status()
        elif forward is not None:
            status = forward
            Game.constructor(player_1_col, player_2_col)
    elif status == "GAME":
        forward, backward, results, winner_col = Game.populate_content()
        if backward is not None:
            status = backward
            Selection.reset_status()
        elif forward is not None:
            status = forward
            Result.constructor(results, winner_col)
    elif status == "RESULT":
        forward, backward, next_turn = Result.populate_content()
        if backward is not None:
            status = backward
            Selection.reset_status()
        elif forward is not None:
            status = forward
            Game.set_turn(next_turn)
            Game.reset_game()

    pygame.display.update()
    clock.tick(60)