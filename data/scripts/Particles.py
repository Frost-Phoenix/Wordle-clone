import random
import pygame as pg


class Particles:
    def __init__(self, display_surface: pg.Surface) -> None:
        self.display_surface = display_surface
        self.particles = []

    def draw(self) -> None:
        def circle_surf(radius, color: tuple) -> pg.Surface:
            surf = pg.Surface((radius * 2, radius * 2))
            pg.draw.circle(surf, color, (radius, radius), radius)
            surf.set_colorkey((0, 0, 0))
            return surf

        if self.particles:
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= particle[3]
                particle[1][1] += 0.15
                pg.draw.circle(self.display_surface, (0, 200, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

                radius = particle[2] * 2
                self.display_surface.blit(circle_surf(radius, (0, 20, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=pg.BLEND_RGB_ADD)

                if particle[2] <= 0:
                    self.particles.remove(particle)

    def add(self, nb: int, pos: tuple, duration: float) -> None:
        for i in range(nb):
            pos_x = pos[0]
            pos_y = pos[1]
            direction_x = random.randint(-3,3)
            direction_y = random.randint(-30, 20) / 10 - 1
            radius = random.randint(5, 8)
            self.particles.append([[pos_x,pos_y],[direction_x,direction_y],radius, duration])