import pygame
import random as rd
import game


class Screen:
    def __init__(self, surface, dimensions: tuple) -> None:
        self.surface = surface
        self.max_width, self.max_height = dimensions
        self.outputs = []  # (<pygame_object>, (x_pos, y_pos))
        self.rects = []  # (<pygame_rect>, colour, width)
        # Standard Colours
        self.PrimaryButtonCol = "#FF768B"
        self.SecondaryButtonCol = "#FFB6C1"
        # Standard Button Dimensions
        self.PrimaryButtonWidth = 150
        self.PrimaryButtonHeight = 55

        self.SecondaryButtonWidth = 125
        self.SecondaryButtonHeight = 45
        return

    def display(self) -> None:
        # Rects
        for rect, col, width in self.rects:
            if width <= 0:
                pygame.draw.rect(self.surface, col, rect)
                continue
            pygame.draw.rect(self.surface, col, rect, width)
        for obj in self.outputs:
            self.surface.blit(*obj)
        self.outputs = []
        self.rects = []

    def create_text(self, text: str, col, size: int, g_pos: tuple, semi_bold=False, justify="left") -> None:
        if semi_bold:
            txt_placeholder = self.OpenSansFont_SemiBold(size).render(text, 1, col)
            txt_rect = txt_placeholder.get_rect()
            pos_placeholder = self.compute_justification(txt_rect.width, txt_rect.height, g_pos, justify)
            self.outputs.append((txt_placeholder, pos_placeholder))
            return
        txt_placeholder = self.OpenSansFont_Regular(size).render(text, 1, col)
        txt_rect = txt_placeholder.get_rect()
        pos_placeholder = self.compute_justification(txt_rect.width, txt_rect.height, g_pos, justify)
        self.outputs.append((txt_placeholder, pos_placeholder))
        return

    def create_rectangle(self, width: int, height: int, g_pos: tuple, col, fill=0, justify="left"):
        pos_placeholder = self.compute_justification(width, height, g_pos, justify)
        rect_placeholder = pygame.Rect(pos_placeholder, (width, height))
        self.rects.append((rect_placeholder, col, fill))
        return rect_placeholder

    @staticmethod
    def OpenSansFont_SemiBold(text_size):
        return pygame.font.Font("OpenSans-Semibold.ttf", text_size)

    @staticmethod
    def OpenSansFont_Regular(text_size):
        return pygame.font.Font("OpenSans-Regular.ttf", text_size)

    @staticmethod
    def compute_justification(width: int, height: int, or_pos: tuple, desired: str) -> tuple:
        x, y = or_pos
        if desired.lower() == "right":
            return x - width, y
        elif desired.lower() == "center":
            return x - width / 2, y - height / 2
        return x, y


class MainScreen(Screen):
    def __init__(self, surface, dimensions: tuple):
        super().__init__(surface, dimensions)

    def populate_content(self):
        self.create_rectangle(width=self.max_width, height=self.max_height, col="light gray", g_pos=(0, 0),
                              justify="left")  # Background
        self.create_rectangle(width=self.max_width - 10, height=self.max_height - 10, col=pygame.Color(255, 105, 180),
                              g_pos=(5, 5), fill=1, justify="left")  # Game Boarder
        self.create_text(text="Tic-Tac-Toe", col=pygame.Color(255, 105, 180), size=50, g_pos=(self.max_width / 2, 150),
                         justify="center", semi_bold=True)  # Game Title

        # Button Texts and Rectangles
        self.create_text(text="Play", col="white", size=36, g_pos=(self.max_width / 2, 300), justify="center",
                         semi_bold=False)  # Play Game
        b_play = self.create_rectangle(width=self.PrimaryButtonWidth, height=self.PrimaryButtonHeight,
                                       col=self.PrimaryButtonCol,
                                       g_pos=(self.max_width / 2, 300), fill=0,
                                       justify="center")  # Play Game - Background
        self.create_rectangle(width=self.PrimaryButtonWidth, height=self.PrimaryButtonHeight, col="white",
                              g_pos=(self.max_width / 2, 300), fill=3,
                              justify="center")  # Play Game - Boarder
        # Quit Button
        # Return Button
        q_x, q_y = self.max_width / 2 - self.SecondaryButtonWidth / 2, 365  # Position for Return Button
        b_quit = self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight,
                                         col=self.SecondaryButtonCol,
                                         g_pos=(q_x, q_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight, col="white",
                              fill=3,
                              g_pos=(q_x, q_y),
                              justify="left")  # Return Button Boarder
        self.create_text(text="Quit", col="white", size=26,
                         g_pos=(q_x + (self.SecondaryButtonWidth / 2), q_y + (self.SecondaryButtonHeight / 2)),
                         justify="center",
                         semi_bold=True)  # Return Button Text

        self.display()

        mx, my = pygame.mouse.get_pos()
        l_click, m_click, r_click = pygame.mouse.get_pressed()
        if b_play.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return "SELECT", None
        if b_quit.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return None, "QUIT"
        return None, None


class CharacterSelectionScreen(Screen):
    def __init__(self, surface, dimensions) -> None:
        super().__init__(surface, dimensions)

        self.char_selected = None
        self.player_one = None
        self.player_two = None

    def populate_content(self):
        # Background
        self.create_rectangle(width=self.max_width, height=self.max_height, col="light gray", g_pos=(0, 0),
                              justify="left")  # Fill
        self.create_rectangle(width=self.max_width - 10, height=self.max_height - 10, col=pygame.Color(255, 105, 180),
                              g_pos=(5, 5), fill=1, justify="left")  # Game Boarder
        # Player Selection Header
        plr_x, plr_y = 125, 75
        if self.player_one is None:  # Player One Has Not Selected a Character Icon
            self.create_text(text="Player One", col="white", size=32, g_pos=(plr_x, plr_y), justify="center",
                             semi_bold=True)  # Player One
            self.create_text(text="Player Two", col="white", size=32, g_pos=(plr_x + 250, plr_y), justify="center",
                             semi_bold=False)  # Player Two
            self.create_text(text="Selecting", col="white", size=20, g_pos=(plr_x, plr_y - 45), justify="center",
                             semi_bold=True)  # Text Header
            self.create_rectangle(width=200, height=65,
                                  col="white",
                                  g_pos=(plr_x, plr_y), fill=3, justify="center")  # Selected Player Box
        else:
            self.create_text(text="Player One", col="white", size=32, g_pos=(plr_x, plr_y), justify="center",
                             semi_bold=False)  # Player One
            self.create_text(text="Player Two", col="white", size=32, g_pos=(plr_x + 250, plr_y), justify="center",
                             semi_bold=True)  # Player Two
            self.create_text(text="Selecting", col="white", size=20, g_pos=(plr_x + 250, plr_y - 45), justify="center",
                             semi_bold=True)  # Text Header
            self.create_rectangle(width=200, height=65,
                                  col="white",
                                  g_pos=(plr_x + 250, plr_y), fill=3, justify="center")  # Selected Player Box
        # Selection Description
        self.create_text(text="Select a character from the options below.", col="white", size=18,
                         g_pos=(self.max_width / 2, 175),
                         justify="center",
                         semi_bold=False)
        # Character Icon List Selection
        char_positions = (
            (62, 240), (62, 240 + 100), (62 + 150, 240), (62 + 150, 240 + 100), (62 + 300, 240), (62 + 300, 240 + 100))
        char_one = self.create_rectangle(width=75, height=75, col="orange",
                                         g_pos=(char_positions[0][0], char_positions[0][1]),
                                         justify="left")
        char_two = self.create_rectangle(width=75, height=75, col="blue",
                                         g_pos=(char_positions[1][0], char_positions[1][1]),
                                         justify="left")
        char_three = self.create_rectangle(width=75, height=75, col="magenta",
                                           g_pos=(char_positions[2][0], char_positions[2][1]),
                                           justify="left")
        char_four = self.create_rectangle(width=75, height=75, col="green",
                                          g_pos=(char_positions[3][0], char_positions[3][1]),
                                          justify="left")
        char_five = self.create_rectangle(width=75, height=75, col="red",
                                          g_pos=(char_positions[4][0], char_positions[4][1]),
                                          justify="left")
        char_six = self.create_rectangle(width=75, height=75, col="black",
                                         g_pos=(char_positions[5][0], char_positions[5][1]),
                                         justify="left")
        char_buttons = ("orange", "blue", "magenta", "green", "red", "black")
        if self.char_selected is not None:
            self.create_rectangle(width=75, height=75, col="white", fill=3,
                                  g_pos=(char_positions[self.char_selected][0], char_positions[self.char_selected][1]),
                                  justify="left")  # Boarder to Represent that this Box is selected
        # Return Button
        r_x, r_y = 35, self.max_height - self.SecondaryButtonHeight - 35  # Position for Return Button
        b_return = self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight,
                                         col=self.SecondaryButtonCol,
                                         g_pos=(r_x, r_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight, col="white",
                              fill=3,
                              g_pos=(r_x, r_y),
                              justify="left")  # Return Button Boarder
        self.create_text(text="Return", col="white", size=24,
                         g_pos=(r_x + (self.SecondaryButtonWidth / 2), r_y + (self.SecondaryButtonHeight / 2)),
                         justify="center",
                         semi_bold=False)  # Return Button Text
        # Select Button
        s_x, s_y = self.max_width - self.SecondaryButtonWidth - 35, self.max_height - self.SecondaryButtonHeight - 35
        b_select = self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight,
                                         col=self.PrimaryButtonCol,
                                         g_pos=(s_x, s_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight, col="white",
                              fill=3,
                              g_pos=(s_x, s_y),
                              justify="left")  # Return Button Boarder
        self.create_text(text="Select", col="white", size=24,
                         g_pos=(s_x + (self.SecondaryButtonWidth / 2), s_y + (self.SecondaryButtonHeight / 2)),
                         justify="center",
                         semi_bold=False)  # Return Button Text

        self.display()

        mx, my = pygame.mouse.get_pos()
        l_click, m_click, r_click = pygame.mouse.get_pressed()
        # Selecting Character
        if char_one.collidepoint(mx, my) and l_click:
            self.char_selected = 0 if (self.char_selected is None) or (self.char_selected != 0) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        elif char_two.collidepoint(mx, my) and l_click:
            self.char_selected = 1 if (self.char_selected is None) or (self.char_selected != 1) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        elif char_three.collidepoint(mx, my) and l_click:
            self.char_selected = 2 if (self.char_selected is None) or (self.char_selected != 1) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        elif char_four.collidepoint(mx, my) and l_click:
            self.char_selected = 3 if (self.char_selected is None) or (self.char_selected != 1) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        elif char_five.collidepoint(mx, my) and l_click:
            self.char_selected = 4 if (self.char_selected is None) or (self.char_selected != 1) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        elif char_six.collidepoint(mx, my) and l_click:
            self.char_selected = 5 if (self.char_selected is None) or (self.char_selected != 1) else None
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        # Return Button Logic
        elif b_return.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return None, "HOME", None, None
        # Select Button Logic
        elif b_select.collidepoint(mx, my) and l_click and self.char_selected is not None:
            if self.player_one is None:
                self.player_one = char_buttons[self.char_selected]
                self.char_selected = None
            elif self.player_two is None:
                self.player_two = char_buttons[self.char_selected]
                self.char_selected = None
            if self.player_one is not None and self.player_two is not None:
                pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
                return "GAME", None, self.player_one, self.player_two
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
        return None, None, None, None

    def reset_status(self):
        self.player_one = None
        self.player_two = None
        self.char_selected = None

class GameScreen(Screen):
    def __init__(self, surface, dimensions):
        super().__init__(surface, dimensions)
        self.start_up = True
        self.player_1_col = None
        self.player_2_col = None

        self.turn = rd.randint(1, 2)  # Determines who Goes First

        # Tile Properties
        self.b_x = 52
        self.b_y = 135
        self.b_col = "#EDAEC0"
        self.b_width = 125
        self.b_height = 125
        self.tiles = []  # List of Tiles

        # Game Properties
        self.g_main = game.TicTacToe()

    def populate_content(self):
        # Checks to See if Game is Over
        status = self.g_main.check_status()
        if status:
            # Insert A New Function for Overlay
            return "RESULT", None, status, self.player_1_col if status == 1 else self.player_2_col
        # Background
        self.create_rectangle(width=self.max_width, height=self.max_height, col="light gray", g_pos=(0, 0),
                              justify="left")  # Fill
        self.create_rectangle(width=self.max_width - 10, height=self.max_height - 10, col=pygame.Color(255, 105, 180),
                              g_pos=(5, 5), fill=1, justify="left")  # Game Boarder
        # Player' Turn Header
        self.create_text(text=f"Player {self.turn}'s Turn", col="white", size=32, g_pos=(self.max_width / 2, 60),
                         justify="center",
                         semi_bold=True)  # Player One
        # Board Grid Lines (Barriers)
        self.create_rectangle(width=10, height=self.b_height * 3 + 20, col="black",
                              g_pos=(self.b_x + self.b_width, self.b_y),
                              justify="left")  # Left Vertical Line
        self.create_rectangle(width=10, height=self.b_height * 3 + 20, col="black",
                              g_pos=(self.b_x + self.b_width * 2 + 10, self.b_y),
                              justify="left")  # Right Vertical Line
        self.create_rectangle(width=self.b_width * 3 + 20, height=10, col="black",
                              g_pos=(self.b_x, self.b_y + self.b_height),
                              justify="left")  # Top Horizontal Line
        self.create_rectangle(width=self.b_width * 3 + 20, height=10, col="black",
                              g_pos=(self.b_x, self.b_y + self.b_height * 2 + 10),
                              justify="left")  # Bottom Horizontal Line
        # Board Tiles
        b_00 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(0, 0),
                                     g_pos=(self.b_x, self.b_y),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x, self.b_y), fill=3, justify="left")  # Game Boarder

        b_01 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(0, 1),
                                     g_pos=(self.b_x + self.b_width + 10, self.b_y),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width + 10, self.b_y), fill=3, justify="left")  # Game Boarder

        b_02 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(0, 2),
                                     g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y), fill=3,
                              justify="left")  # Game Boarder

        b_10 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(1, 0),
                                     g_pos=(self.b_x, self.b_y + self.b_height + 10),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x, self.b_y + self.b_height + 10), fill=3, justify="left")  # Game Boarder

        b_11 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(1, 1),
                                     g_pos=(self.b_x + self.b_width + 10, self.b_y + self.b_height + 10),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width + 10, self.b_y + self.b_height + 10), fill=3,
                              justify="left")  # Game Boarder

        b_12 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(1, 2),
                                     g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y + self.b_height + 10),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y + self.b_height + 10), fill=3,
                              justify="left")  # Game Boarder

        b_20 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(2, 0),
                                     g_pos=(self.b_x, self.b_y + self.b_height * 2 + 20),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x, self.b_y + self.b_height * 2 + 20), fill=3,
                              justify="left")  # Game Boarder

        b_21 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(2, 1),
                                     g_pos=(self.b_x + self.b_width + 10, self.b_y + self.b_height * 2 + 20),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width + 10, self.b_y + self.b_height * 2 + 20), fill=3,
                              justify="left")  # Game Boarder

        b_22 = self.create_rectangle(width=self.b_width, height=self.b_height, col=self.compute_col(2, 2),
                                     g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y + self.b_height * 2 + 20),
                                     justify="left")  # Fill
        self.create_rectangle(width=self.b_width, height=self.b_height, col=pygame.Color(255, 105, 180),
                              g_pos=(self.b_x + self.b_width * 2 + 20, self.b_y + self.b_height * 2 + 20), fill=3,
                              justify="left")  # Game Boarder
        # Return Button
        r_x, r_y = 15, self.max_height - self.SecondaryButtonHeight - 5  # Position for Return Button
        b_return = self.create_rectangle(width=self.SecondaryButtonWidth - 10, height=self.SecondaryButtonHeight - 10,
                                         col=self.SecondaryButtonCol,
                                         g_pos=(r_x, r_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth - 10, height=self.SecondaryButtonHeight - 10, col="white",
                              fill=3,
                              g_pos=(r_x, r_y),
                              justify="left")  # Return Button Boarder
        self.create_text(text="Return", col="white", size=18,
                         g_pos=(r_x + ((self.SecondaryButtonWidth - 10) / 2), r_y + ((self.SecondaryButtonHeight - 10)/ 2)),
                         justify="center",
                         semi_bold=False)  # Return Button Text
        # Adds Elements to A List where we know which Tiles can be Pressed
        if self.start_up:
            self.start_up = False
            self.tiles = [b_00, b_01, b_02, b_10, b_11, b_12, b_20, b_21, b_22]

        self.display()
        # User-interactions
        mx, my = pygame.mouse.get_pos()
        l_click, m_click, r_click = pygame.mouse.get_pressed()
        # Selecting Return Button
        if b_return.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return None, "HOME", None, None
        # Selecting Tiles
        if b_00.collidepoint(mx, my) and l_click and b_00 in self.tiles:
            self.tiles.remove(b_00)
            self.g_main.make_move(0, 0, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_01.collidepoint(mx, my) and l_click and b_01 in self.tiles:
            self.tiles.remove(b_01)
            self.g_main.make_move(0, 1, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_02.collidepoint(mx, my) and l_click and b_02 in self.tiles:
            self.tiles.remove(b_02)
            self.g_main.make_move(0, 2, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2

        elif b_10.collidepoint(mx, my) and l_click and b_10 in self.tiles:
            self.tiles.remove(b_10)
            self.g_main.make_move(1, 0, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_11.collidepoint(mx, my) and l_click and b_11 in self.tiles:
            self.tiles.remove(b_11)
            self.g_main.make_move(1, 1, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_12.collidepoint(mx, my) and l_click and b_12 in self.tiles:
            self.tiles.remove(b_12)
            self.g_main.make_move(1, 2, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2

        elif b_20.collidepoint(mx, my) and l_click and b_20 in self.tiles:
            self.tiles.remove(b_20)
            self.g_main.make_move(2, 0, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_21.collidepoint(mx, my) and l_click and b_21 in self.tiles:
            self.tiles.remove(b_21)
            self.g_main.make_move(2, 1, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        elif b_22.collidepoint(mx, my) and l_click and b_22 in self.tiles:
            self.tiles.remove(b_22)
            self.g_main.make_move(2, 2, self.turn)  # Make Move
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            self.turn = 1 if self.turn == 2 else 2
        return None, None, None, None

    def compute_col(self, row, col) -> str:
        position_val = self.g_main.board[row][col]
        if position_val == 1:
            return self.player_1_col
        elif position_val == 2:
            return self.player_2_col
        return self.b_col

    def constructor(self, player_1_col, player_2_col):
        self.player_1_col = player_1_col
        self.player_2_col = player_2_col

    def set_turn(self, turn):
        self.turn = turn

    def reset_game(self):
        self.g_main.reset_board()
        self.start_up = True

class ResultScreen(Screen):
    def __init__(self, surface, dimensions):
        super().__init__(surface, dimensions)
        self.results = None
        self.winner_col = None

    def populate_content(self):
        # Background
        self.create_rectangle(width=self.max_width, height=self.max_height, col="light gray", g_pos=(0, 0),
                              justify="left")  # Fill
        self.create_rectangle(width=self.max_width - 10, height=self.max_height - 10, col=pygame.Color(255, 105, 180),
                              g_pos=(5, 5), fill=1, justify="left")  # Game Boarder
        # Result Header
        if self.results == "Draw":
            self.create_text(text=f"{self.results}!", col="white", size=40, g_pos=(self.max_width / 2, 150),
                             justify="center",
                             semi_bold=True)  # Draw
        else:
            self.create_text(text=f"{self.results} has won!", col="white", size=40, g_pos=(self.max_width / 2, 150),
                             justify="center",
                             semi_bold=True)  # Player 'n' Won
        # Play Again Button
        s_x, s_y = self.max_width / 2 - self.SecondaryButtonWidth / 2, 250
        b_again = self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight,
                                         col=self.PrimaryButtonCol,
                                         g_pos=(s_x, s_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight, col="white",
                              fill=3,
                              g_pos=(s_x, s_y),
                              justify="left")  # Play Again Button Boarder
        self.create_text(text="Play Again", col="white", size=22,
                         g_pos=(s_x + (self.SecondaryButtonWidth / 2), s_y + (self.SecondaryButtonHeight / 2)),
                         justify="center",
                         semi_bold=True)  # Play Button Text
        # Return Home Button
        r_x, r_y = self.max_width / 2 - self.SecondaryButtonWidth / 2, 325  # Position for Return Button
        b_return = self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight,
                                         col=self.SecondaryButtonCol,
                                         g_pos=(r_x, r_y),
                                         justify="left")
        self.create_rectangle(width=self.SecondaryButtonWidth, height=self.SecondaryButtonHeight, col="white",
                              fill=3,
                              g_pos=(r_x, r_y),
                              justify="left")  # Return Button Boarder
        self.create_text(text="Return", col="white", size=24,
                         g_pos=(
                         r_x + (self.SecondaryButtonWidth / 2), r_y + (self.SecondaryButtonHeight / 2)),
                         justify="center",
                         semi_bold=True)  # Return Button Text

        self.display()

        # User-interactions
        mx, my = pygame.mouse.get_pos()
        l_click, m_click, r_click = pygame.mouse.get_pressed()
        # Play Again Button
        if b_again.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return "GAME", None, self.compute_next_turn(self.results)
        # Return Button
        if b_return.collidepoint(mx, my) and l_click:
            pygame.time.delay(150)  # Pauses Program for 150 ms (prevent double hitting)
            return None, "HOME", None
        return None, None, None

    def constructor(self, results, winner_col):
        self.results = self.compute_results(results)
        self.winner_col = winner_col

    @staticmethod
    def compute_results(value) -> str:
        if value == 1:
            return "Player 1"
        elif value == 2:
            return "Player 2"
        return "Draw"

    @staticmethod
    def compute_next_turn(value):
        if value == "Player 1":
            return 2
        if value == "Player 2":
            return 1
        return None

