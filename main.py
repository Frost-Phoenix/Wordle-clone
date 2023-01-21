import pygame as pg
import sys
#------------------------------------------------------
from data.scripts.Game import Game
from data.scripts.Utils import resource_path, WINDOW_WIDTH, WINDOW_HEIGHT


def main() -> None:

    pg.init()

    pg.display.set_caption("Motus")
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_icon = pg.image.load(resource_path(r"data/images/icon/logo.png"))
    pg.display.set_icon(game_icon)    
    window.fill((0,0,120))
    clock = pg.time.Clock()

    # Game variable
    FPS = 60
    game = Game(window)

    game_runing = True
    while game_runing:

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key >= 97 and event.key <= 122: game.key_down(chr(event.key).upper())
                elif event.key == pg.K_RETURN: game.key_down("enter")
                elif event.key == pg.K_BACKSPACE: game.key_down("delet")
            elif event.type == pg.KEYUP:
                if event.key >= 97 and event.key <= 122: game.use_key(chr(event.key).upper())
                elif event.key == pg.K_RETURN: game.use_key("enter")
                elif event.key == pg.K_BACKSPACE: game.use_key("delet")
                elif event.key == pg.K_HOME: game.use_key("replay")

        # window.fill((14,14,15))
        window.fill((20,20,22))
        
        game.update()

        pg.display.set_caption("Motus : " + str(int(clock.get_fps())) + " fps")

        pg.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

