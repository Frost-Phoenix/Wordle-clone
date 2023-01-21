import pygame as pg 
#------------------------------------------------------
from data.scripts.Utils import import_folder


class Button:

    def __init__(self, pos: tuple, images_path: str, action) -> None: # action: function

        # Variables
        self.is_clicked = False
        self.action = action
        self.base_pos = pos

        # Setup
        self.import_images(images_path)
        self.change_image("n")
        self.rect = self.image.get_rect(topleft = pos)
        self.colide_rect = self.rect.copy()

    def import_images(self, images_path: str) -> None:
        self.frames = import_folder(images_path)

    def change_image(self, state: str) -> None:
        if state == "c": self.image = self.frames[0]        
        elif state == "n": self.image = self.frames[1]
        elif state == "s": self.image = self.frames[2]

        self.state = state

    def check_mouse_colision(self) -> None:
        mouse_pos = pg.mouse.get_pos()

        if self.colide_rect.collidepoint(mouse_pos):
            self.check_click()
            if not self.is_clicked and self.state != "s": 
                self.change_image("s")
                if self.rect.y != self.base_pos[1]: self.rect.y = self.base_pos[1]

        elif self.state != "n":
            self.is_clicked = False
            self.change_image("n")
            if self.rect.y != self.base_pos[1]: self.rect.y = self.base_pos[1]

    def check_click(self) -> None:
        mouse_clic = pg.mouse.get_pressed()[0]

        if mouse_clic:
            if not self.is_clicked:
                self.change_image("c")
                if self.rect.y == self.base_pos[1]: self.rect.y += 2
                self.is_clicked = True
        elif self.is_clicked:
            self.is_clicked = False
            self.action()

    def update(self) -> None:
        self.check_mouse_colision()


class Close_button(Button):

    def __init__(self, pos: tuple, action) -> None: # action: function
        super().__init__(pos, r"data/images/gui/buttons/close", action)

        self.colide_rect.x += 74
        self.colide_rect.y += 77

class Stats_button(Button):

    def __init__(self, pos: tuple, action) -> None: # action: function
        super().__init__(pos, r"data/images/gui/buttons/stats", action)

class Replay_button(Button):

    def __init__(self, pos: tuple, action) -> None: # action: function
        super().__init__(pos, r"data/images/gui/buttons/replay", action)