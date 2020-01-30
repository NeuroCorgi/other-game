# Basic game view
import os

from server import RequestsHandler

import pygame as pg
clock = pg.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    image = pg.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ships(pg.sprite.Sprite):
    image = load_image('ship_image.png')

    def __init__(self, group, coords):
        super().__init__(group)
        self.image = Ships.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def update(self, coords):
        self.rect.move(*coords)


class Station(pg.sprite.Sprite): 
    image = load_image('station_image.png')

    def __init__(self, group, coords):
        super().__init__(group)
        self.image = Station.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class Window:

    def __init__(self, surface, location):
        self.surface = surface

        self.moving = (0, 0)

        self.ships = pg.sprite.Group()
        self.stations = pg.sprite.Group()
    
    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.KEY == pg.K_UP or event.key == pg.K_w:
                self.moving[0] = -1
            if event.KEY == pg.K_DOWN or event.key == pg.K_s:
                self.moving[0] = 1
            if event.KEY == pg.K_LEFT or event.key == pg.K_a:
                self.moving[1] = -1
            if event.KEY == pg.K_RIGHT or event.key == pg.K_d:
                self.moving[1] = 1
        if event.type == pg.KEYUP:
            if event.KEY == pg.K_UP or event.key == pg.K_w or event.KEY == pg.K_DOWN or event.key == pg.K_s:
                self.moving[0] = 0
            if event.KEY == pg.K_LEFT or event.key == pg.K_a or event.KEY == pg.K_RIGHT or event.key == pg.K_d:
                self.moving[1] = 0

    def show(self):
        while True:
            for event in pg.event.get():
                self.handle_event(event)
            self.surface.fill(0, 0, 0)

            self.ships.draw(self.surface)
            self.stations.draw(self.surface)
            clock.tick(60)
        