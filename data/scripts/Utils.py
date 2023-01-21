import sys, pickle
import pygame as pg
from os import walk, path

WINDOW_WIDTH = 495
WINDOW_HEIGHT = 700

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

def import_sprite(path: str) -> pg.Surface:
    image_surface = pg.image.load(resource_path(resource_path(path))).convert_alpha()
    
    return image_surface

def import_folder(path: str) -> list:
    surface_list = []
    path = resource_path(path)
    
    for _,__,imgs_files in walk(resource_path(path)):
        for image in imgs_files:
            full_path = path + "/" + image
            image_surface = pg.image.load(resource_path(full_path)).convert_alpha()
            surface_list.append(image_surface)

    return surface_list

def import_scores() -> dict:
    if path.isfile(resource_path(r"data/scores")):
        with open(resource_path(r"data/scores"), "rb") as f: scores = pickle.load(f)
    else: scores = {"nb_games": 0, "nb_win": 0, "nb_guess": [0]*7, "win_streak": 0}

    return scores

def save_scores(scores: dict) -> None:
    with open(resource_path(r"data/scores"), "wb") as f: pickle.dump(scores, f)