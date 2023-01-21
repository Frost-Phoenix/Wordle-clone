import pygame as pg
import math
from random import randint
#------------------------------------------------------
from data.scripts.Utils import import_sprite, resource_path


class Letter_cell(pg.sprite.Sprite):

    def __init__(self, pos: tuple, grid_pos: list, particles) -> None: # particles: class Particles
        super().__init__()

        # Variables
        self.letter = None
        self.pos = pos
        self.grid_pos = grid_pos
        self.particles = particles
        self.is_shaking = False
        self.shake_duration = 0
        self.is_anim = False
        self.animation_timer = 0
        self.font = pg.font.Font(resource_path(r"data/font/upheavtt.ttf"), 36) 

        # Images
        self.import_frames()
        self.change_image("unselected")
        self.rect = self.image.get_rect(topleft = self.pos)

    def import_frames(self) -> None:
        selected_frame = import_sprite(r"data/images/cells/selected_cell.png")
        unselected_frame = import_sprite(r"data/images/cells/unselected_cell.png")
        filled_frame = import_sprite(r"data/images/cells/filled.png")
        normal_frames = import_sprite(r"data/images/cells/normal.png")
        green_frames = import_sprite(r"data/images/cells/green.png")
        orange_frames = import_sprite(r"data/images/cells/orange.png")

        self.frames = {"selected": selected_frame, "unselected": unselected_frame, "filled": filled_frame, "normal": normal_frames, "green":green_frames, "orange":orange_frames}

    def change_image(self, state: str) -> None:
        self.image = self.frames[state].copy()

        if self.letter != None:
            letter_txt = self.font.render(self.letter, False, "white")
            self.image.blit(letter_txt, letter_txt.get_rect(center = (26,23)))

        self.state = state

    def shake(self) -> None:
        if self.shake_duration > 0:
            self.shake_duration -= 1
            self.rect.x = self.pos[0] + randint(-5,5)
        else:
            self.is_shaking = False
            self.rect.x = self.pos[0]

    def reveal_anim(self) -> None:
        if self.angle >= 180 and self.state == "filled": 
            self.angle = 0
            self.change_image(self.next_state)
            self.base_image = self.image
        elif self.angle >= 90 and self.state != "filled": 
            self.is_anim = False
            self.image = self.base_image
            self.rect = self.image.get_rect(topleft = self.pos)
            if self.state == "green": self.particles.add(30,self.rect.center, 0.18)
        
        if self.is_anim:
            new_height = round(math.sin(math.radians(self.angle)) * 50) 
            self.angle += 8
            tmp_image = self.base_image if new_height >= 0 else pg.transform.flip(self.base_image, False, True) 
            self.image = pg.transform.scale(tmp_image, (50, abs(new_height)))
            self.rect = self.image.get_rect(center = (self.pos[0]+25,self.pos[1]+25))

    def start_anim(self, next_state: str, timer: int) -> None:
        self.angle = 90
        self.is_anim = True
        self.animation_timer = timer
        self.next_state = next_state
        self.base_image = self.image

    def update(self) -> None:
        if self.is_shaking: self.shake()
        elif self.is_anim:
            if self.animation_timer == 0: self.reveal_anim()
            else: self.animation_timer -= 1