import pygame as pg 
#------------------------------------------------------
from data.scripts.Utils import import_sprite, WINDOW_WIDTH


class Message_box(pg.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()

        # Variables
        self.is_show = False
        self.show_duration = 0

        self.import_images()

    def import_images(self) -> None:
        word_not_found_surface = import_sprite(r"data/images/gui/messages_box/word_not_found.png")
        to_short_surface = import_sprite(r"data/images/gui/messages_box/to_short.png")

        self.messages_box = {"word_not_found": word_not_found_surface, "to_short": to_short_surface}

    def change_image(self, message_box: str) -> None:
        self.image = self.messages_box[message_box].copy()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH//2, 30)) # 82

    def show(self, message_box: str) -> None:
        self.change_image(message_box)
        self.is_show = True
        self.show_duration = 15
        self.alpha = 255

    def drop_down(self) -> None:
        if self.rect.center[1] < 55: self.rect.y += 4
        elif self.rect.center[1] < 70: self.rect.y += 2
        else: self.rect.y += 1
    
    def fade_out(self) -> None:
        self.image.set_alpha(self.alpha)
        self.alpha -= 10
        if self.alpha <= 0: self.is_show = False

    def update(self) -> None:
        if self.is_show: 
            if self.rect.center[1] < 82: self.drop_down()
            elif self.show_duration > 0: self.show_duration -= 1
            else: self.fade_out()