import pygame as pg
#------------------------------------------------------
from data.scripts.Motus import *
from data.scripts.Keys import Key
from data.scripts.Letter_cell import Letter_cell
from data.scripts.Messages_box import Message_box
from data.scripts.Stats_panel import Stats_panel
from data.scripts.Buttons import Replay_button, Stats_button
from data.scripts.Particles import Particles
from data.scripts.Utils import import_scores, import_sprite, WINDOW_WIDTH, WINDOW_HEIGHT, save_scores, resource_path


class Game:

    def __init__(self, display_surface: pg.Surface) -> None:

        # Variables
        self.display_surface = display_surface
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.game_state = "end_game"
        self.scores = import_scores()

        # Images
        self.title_surface = import_sprite(resource_path(r"data/images/gui/title.png"))
        self.title_rect = self.title_surface.get_rect(center = (self.WINDOW_WIDTH//2, 55//2))
        self.stats_panel = Stats_panel(self.display_surface, self.change_game_state)
        self.stats_button = Stats_button((38,12), self.show_stats_panel)
        self.replay_button = Replay_button((WINDOW_WIDTH-70,12), self.start_game)

        # Pygame sprites groups
        self.keys = pg.sprite.Group()
        self.message_box = pg.sprite.GroupSingle()
        self.particles = Particles(self.display_surface)

        # Game initialisation
        self.create_keyboard()
        self.import_messages_box()
        self.word_list = import_word_list()

        # Start a new game
        self.start_game()

    def start_game(self) -> None:
        if self.game_state != "end_game": self.scores["win_streak"] = 0

        self.word = choose_word(self.word_list)
        self.guess_word = ""
        self.selected_cell = [0,0]
        self.game_state = "play"

        self.creat_letter_cells()
        for cell in self.letter_cells:
            if cell.grid_pos == self.selected_cell: cell.change_image("selected")

        for key_button in self.keys: key_button.change_image("normal", "n")

        print(self.word)

    def creat_letter_cells(self) -> None:
        self.letter_cells = pg.sprite.Group()

        nb_col = len(self.word)
        y = 110

        for row in range(6):
            x = (self.WINDOW_WIDTH - (nb_col * 58) + 8) // 2
            for col in range(nb_col):
                cell = Letter_cell((x,y), [row, col], self.particles)
                self.letter_cells.add(cell)
                x += 58
            y += 58

    def create_keyboard(self) -> None:

        letters = "AZERTYUIOPQSDFGHJKLMWXCVBN"
        letter = 0
        start_x = [10,10,106]

        for y in range(self.WINDOW_HEIGHT - 5 - (65*3), self.WINDOW_HEIGHT - 10, 65):
            for x in range(start_x[letter//10], 450, 48):
                if len(letters) > letter:
                    key = Key(letters[letter], (x,y), self.use_key)
                    self.keys.add(key)
                    letter += 1

        self.keys.add(Key("delet", (10, self.WINDOW_HEIGHT - 70), self.use_key))
        self.keys.add(Key("enter", (394, self.WINDOW_HEIGHT - 70), self.use_key))

    def import_messages_box(self) -> None:
        box = Message_box()
        self.message_box.add(box)

    def change_game_state(self, state: str) -> None:
        self.game_state = state

    def show_stats_panel(self, show_delay=0, game_score=None) -> None: # show_delay: int, game_score: int
        if game_score == None and self.game_state != "end_game": self.stats_panel.show(self.scores, show_delay, "play")
        else: self.stats_panel.show(self.scores, show_delay, "end_game", game_score)
        self.game_state = "stats_panel"

    def use_key(self, letter: str) -> None:

        def use_letter() -> None:
            for cell in self.letter_cells:
                if cell.grid_pos == self.selected_cell:
                    cell.letter = letter
                    cell.change_image("filled")
                if cell.grid_pos[0] == self.selected_cell[0] and cell.grid_pos[1] == self.selected_cell[1] + 1:
                    cell.change_image("selected")

            self.guess_word += letter
            self.selected_cell[1] += 1

        def use_enter() -> None:
            if len(self.guess_word) == len(self.word) and is_word_in_list(self.guess_word, self.word_list):
                letters_color = check_letters_pos(self.word, self.guess_word)

                anim_timer = 0 
                for cell in self.letter_cells:
                    if cell.grid_pos[0] == self.selected_cell[0]: 
                        color = letters_color[cell.grid_pos[1]]
                        if color == "-": color = "normal"                    
                        cell.start_anim(color, anim_timer)
                        anim_timer += 12

                for key_button in self.keys:
                    if key_button.letter in self.guess_word:
                        color = letters_color[self.guess_word.index(key_button.letter)]
                        if key_button.state[0] == "normal": 
                            if color == "-": key_button.change_image("wrong")
                            else: key_button.change_image(color, "n")
                        elif key_button.state[0] == "orange" and color == "green": 
                            key_button.change_image(color, "n")                            

                win = check_word(self.word, self.guess_word)
                if win or self.selected_cell[0] == 5: # Win / Lose
                    self.scores["nb_games"] += 1

                    if win:
                        self.scores["nb_win"] += 1
                        self.scores["win_streak"] += 1
                        game_score = self.selected_cell[0]
                    else: 
                        game_score = 6
                        self.scores["win_streak"] = 0

                    self.scores["nb_guess"][game_score] += 1

                    save_scores(self.scores)
                    self.show_stats_panel(anim_timer + 20, game_score)
                else:
                    self.guess_word = ""
                    self.selected_cell = [self.selected_cell[0] + 1, 0]

                    for cell in self.letter_cells:
                        if cell.grid_pos == self.selected_cell: cell.change_image("selected")

            else: 
                if len(self.guess_word) < len(self.word): self.message_box.sprite.show("to_short")
                else: self.message_box.sprite.show("word_not_found")
                self.shake_letter_cell_line(self.selected_cell[0])

        def use_delete() -> None:
            self.guess_word = self.guess_word[:len(self.guess_word)-1]

            for cell in self.letter_cells:
                if cell.grid_pos == self.selected_cell:
                    cell.change_image("unselected")
                if cell.grid_pos[0] == self.selected_cell[0] and cell.grid_pos[1] == self.selected_cell[1] - 1:
                    cell.letter = None
                    cell.change_image("selected")

            self.selected_cell[1] -= 1

        if self.game_state == "play":
            if len(letter) == 1 and len(self.guess_word) < len(self.word): use_letter()
            elif letter == "enter": use_enter()
            elif letter == "delet" and len(self.guess_word) > 0: use_delete()
            elif letter == "replay": self.start_game()
            
            for key_button in self.keys:
                if key_button.letter == letter and key_button.state[0] != "wrong":
                    key_button.key_pressed = False
                    key_button.change_image(key_button.state[0], "n")
                    if key_button.rect.y != key_button.base_pos[1]: key_button.rect.y = key_button.base_pos[1]
        
    def key_down(self, letter: str) -> None:
        if self.game_state == "play":
            for key_button in self.keys:
                if key_button.letter == letter and key_button.state[0] != "wrong":
                    if key_button.rect.y == key_button.base_pos[1]: key_button.rect.y += 2
                    key_button.key_pressed = True
                    key_button.change_image(key_button.state[0], "c")

    def shake_letter_cell_line(self, line: int) -> None:
        for cell in self.letter_cells:
            if cell.grid_pos[0] == line: 
                cell.is_shaking = True
                cell.shake_duration = 25

    def draw_game_frame(self) -> None:
        pg.draw.rect(self.display_surface, "#1d1d20", (0,0,self.WINDOW_WIDTH, 55))
        self.display_surface.blit(self.title_surface, self.title_rect)

    def update(self) -> None:
        if self.game_state == "play":
            self.keys.update()
        
        if self.game_state != "stats_panel":
            self.stats_button.update()
            self.replay_button.update()
        
        if self.message_box.sprite.is_show: 
            self.message_box.update()
            self.message_box.draw(self.display_surface)

        self.draw_game_frame()
        self.display_surface.blit(self.stats_button.image, self.stats_button.rect)
        self.display_surface.blit(self.replay_button.image, self.replay_button.rect)

        self.keys.draw(self.display_surface)
        self.letter_cells.update()
        self.letter_cells.draw(self.display_surface)


        self.particles.draw()

        if self.stats_panel.is_show:
            self.stats_panel.update()
            self.stats_panel.draw()