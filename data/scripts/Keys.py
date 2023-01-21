import pygame as pg
#------------------------------------------------------
from data.scripts.Utils import import_folder, import_sprite, resource_path


class Key(pg.sprite.Sprite):

    def __init__(self, letter: str, pos: tuple, action) -> None: # action: function
        super().__init__()
    
        # Variables
        self.letter = letter
        self.action = action
        self.base_pos = pos
        self.is_clicked = False
        self.key_pressed = False
        self.font = pg.font.Font(resource_path(r"data/font/upheavtt.ttf"), 31)
        
        # Images
        self.setup_image()
        self.rect = self.image.get_rect(topleft = pos)

    def setup_image(self) -> None:
        if len(self.letter) == 1: self.import_frames()
        elif self.letter == "enter":
            frames = import_folder(r"data/images/keyboard_keys/enter")
            self.frames = {"normal": frames}
        elif self.letter == "delet":
            frames = import_folder(r"data/images/keyboard_keys/delet")
            self.frames = {"normal": frames}
        
        self.change_image("normal", "n")

    def import_frames(self) -> None:
        normal_frames = import_folder(r"data/images/keyboard_keys/normal")
        green_frames = import_folder(r"data/images/keyboard_keys/green")
        orange_frames = import_folder(r"data/images/keyboard_keys/orange")
        wrong_frame = import_sprite(r"data/images/keyboard_keys/wrong.png")

        self.frames = {"normal": normal_frames, "green":green_frames, "orange":orange_frames, "wrong": wrong_frame}

    def change_image(self, color: tuple, state=None) -> None:
        if state != None:
            if state == "c": self.image = self.frames[color][0]        
            elif state == "n": self.image = self.frames[color][1]
            elif state == "s": self.image = self.frames[color][2]
        else: self.image = self.frames[color]

        if len(self.letter) == 1:
            letter_txt = self.font.render(self.letter, False, "white")
            self.image.blit(letter_txt, letter_txt.get_rect(center = (22,28)))

        self.state = [color, state]

    def check_mouse_colision(self) -> None:
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.check_click()
            if self.state[0] != "wrong":
                if not self.is_clicked and (self.state[1] == "n" or self.state[1] == "c"):
                    self.change_image(self.state[0], "s")
                    if self.rect.y != self.base_pos[1]: self.rect.y = self.base_pos[1]

        elif self.state[1] == "s" or self.state[1] == "c":
            self.is_clicked = False
            self.change_image(self.state[0], "n")
            if self.rect.y != self.base_pos[1]: self.rect.y = self.base_pos[1]

    def check_click(self) -> None:
        # Detect left click
        mouse_clic = pg.mouse.get_pressed()[0]

        if mouse_clic:
            if not self.is_clicked:
                if self.state[0] != "wrong":
                    self.change_image(self.state[0], "c")
                    if self.rect.y == self.base_pos[1]: self.rect.y += 2
                self.is_clicked = True
        elif self.is_clicked:
            self.action(self.letter)
            self.is_clicked = False

    def update(self) -> None:
        if not self.key_pressed: self.check_mouse_colision()