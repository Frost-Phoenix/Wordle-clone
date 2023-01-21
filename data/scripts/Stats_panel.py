import enum
import pygame as pg 
#------------------------------------------------------
from data.scripts.Utils import import_folder, import_sprite, WINDOW_WIDTH, WINDOW_HEIGHT, resource_path
from data.scripts.Buttons import Close_button


class Stats_panel:

    def __init__(self, display_surface: pg.Surface, change_game_state) -> None: # change_game_state: function

        # Variables
        self.bg_surface = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_surface.set_alpha(0)
        self.display_surface = display_surface
        self.bg_alpha = 0
        self.is_show = False
        self.show_delay = 0
        self.state = "hide"
        self.change_game_state = change_game_state
        self.font = pg.font.Font(resource_path(r"data/font/upheavtt.ttf"), 45) 
        self.smal_font = pg.font.Font(resource_path(r"data/font/upheavtt.ttf"), 18) 

        # Button
        self.close_button = Close_button((304,21), self.hide)

        # Setup
        self.import_images()

    def import_images(self) -> None:
        stats_panel_surface = import_sprite(r"data/images/gui/stats_panel.png")
        stats_panel_rect = stats_panel_surface.get_rect(midbottom = (WINDOW_WIDTH//2, -25)) # 275
        self.panel = [stats_panel_surface,stats_panel_rect]

    def add_text(self, txt: str, pos: tuple) -> None:
        txt_surface = self.font.render(txt, False, (60,200,60))
        self.stats_panel_surface.blit(txt_surface, txt_surface.get_rect(center = pos))

    def draw_stat_bar(self, y: int, width: int, nb: int, color: tuple) -> None:
        pg.draw.rect(self.stats_panel_surface, color, (40, y, width, 17), border_radius=3)
        txt_surface = self.smal_font.render(nb, True, "white")
        if nb == "1": nb_x = width + 30
        elif len(nb) == 2: 
            if nb == "11": nb_x = width + 25
            elif nb[0] == "1": nb_x = width + 19
            else: nb_x = width + 13
        else: nb_x = width + 24
        self.stats_panel_surface.blit(txt_surface, (nb_x,y-1)) 

    def add_scores_to_panel(self, scores: dict, game_score: int) -> None:
        def draw_numbers() -> None:
            self.add_text(str(scores["nb_games"]), (72,90))
            if scores["nb_win"] == 0: self.add_text("-", (175,90))
            else: self.add_text(str(round(scores["nb_win"] / scores["nb_games"] * 100)), (175,90))
            self.add_text(str(scores["win_streak"]), (277,90))

        def draw_stats_graph() -> None:
            hightest_nb_guess = max(scores["nb_guess"])
            y = 208
            for nb_guess, nb in enumerate(scores["nb_guess"]):
                if nb != 0:
                    width = 280 * (nb/hightest_nb_guess)
                    if nb_guess == game_score: 
                        if nb_guess == 6: self.draw_stat_bar(y, width, str(nb), (190,0,0))
                        else: self.draw_stat_bar(y, width, str(nb), (25,175,25))
                    else: self.draw_stat_bar(y, width, str(nb), (58,58,60))
                y += 25

        draw_numbers()
        draw_stats_graph()

    def show(self, scores: dict, show_delay: int, next_game_state: str, game_score=None) -> None: # game_score: int
        self.is_show = True
        self.state = "showing"
        self.next_game_state = next_game_state
        self.show_delay = show_delay

        self.stats_panel_surface = self.panel[0].copy()
        self.stats_panel_rect = self.panel[1].copy()
        self.add_scores_to_panel(scores, game_score)
        self.bg_alpha = 0

    def hide(self) -> None:
        self.state = "hiding"
    
    def update(self) -> None:
        def move_panel(direction: str) -> None:
            if direction == "down":
                if self.stats_panel_rect.y < -73: self.stats_panel_rect.y += 15
                elif self.stats_panel_rect.y < 7: self.stats_panel_rect.y += 10
                elif self.stats_panel_rect.y < 37: self.stats_panel_rect.y += 8
                elif self.stats_panel_rect.y < 57: self.stats_panel_rect.y += 5
                elif self.stats_panel_rect.y < 67: self.stats_panel_rect.y += 3
                elif self.stats_panel_rect.y < 77: self.stats_panel_rect.y += 1
                else: self.state = "is_show"
            elif direction == "up":
                if self.stats_panel_rect.y > -274: self.stats_panel_rect.y -= 15
                elif self.stats_panel_rect.y > -354: self.stats_panel_rect.y -= 10
                elif self.stats_panel_rect.y > -384: self.stats_panel_rect.y -= 8
                elif self.stats_panel_rect.y > -404: self.stats_panel_rect.y -= 5
                elif self.stats_panel_rect.y > -414: self.stats_panel_rect.y -= 3
                elif self.stats_panel_rect.y > -424: self.stats_panel_rect.y -= 1
                else: 
                    self.state = "hide"
                    self.is_show = False
                    self.close_button.change_image("n")
                    self.change_game_state(self.next_game_state)

        def change_bg_alpha() -> None:
            if self.state == "showing":
                if self.bg_alpha < 200:
                    self.bg_alpha += 5
                    self.bg_surface.set_alpha(self.bg_alpha)
            elif self.state == "hiding":
                if self.bg_alpha > 0:
                    self.bg_alpha -= 5
                    self.bg_surface.set_alpha(self.bg_alpha)

        if self.state == "showing":
            if self.show_delay == 0:
                move_panel("down")
                change_bg_alpha()
            else: self.show_delay -= 1
        elif self.state == "is_show":
            self.close_button.update()
        elif self.state == "hiding":
            change_bg_alpha()
            move_panel("up")

    def draw(self) -> None:
        self.display_surface.blit(self.bg_surface, (0,0))
        self.display_surface.blit(self.stats_panel_surface, self.stats_panel_rect)
        self.stats_panel_surface.blit(self.close_button.image, self.close_button.rect)