# View for the game map
import sys

from views.view import View

import pygame as pg
from pygame import Color


class Location(pg.sprite.Sprite):

    def __init__(self, group, coords, color, number):
        super().__init__(group)
        self.number = number

        self.image = pg.Surface((40, 40))
        pg.draw.circle(self.image, color, (20, 20), 20)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def handle_pos(self, coords):
        x, y = map(lambda x, y: x - y, coords, (self.rect.x + 20, self.rect.y + 20))
        if x ** 2 + y ** 2 <= 400:
            return self.number
        return False


class MapView(View):

    def __init__(self, surface, data):
        super().__init__(surface, data)
        self.location = data['position']['location']

        self.locations = pg.sprite.Group()

        coords = {
            1: (360, 220), 2: (210, 460), 3: (330, 680), 4: (670, 130), 5: (430, 440),
            6: (1130, 550), 7: (730, 490), 8: (590, 770), 9: (1400, 130), 10: (1680, 530),
        }

        self.graph = {
            1: (2, 4, 5), 2: (1, 5, 3), 3: (2, 5, 8), 4: (1, 5, 7), 5: (1, 2, 3, 4),
            6: (7,), 8: (3, 7)
        }

        for i in range(1, 11):
            Location(self.locations, coords[i], 
                     Color('lightgreen') if i == self.location else Color('dodgerblue3'), i)
    
    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
        if event.type == pg.MOUSEBUTTONDOWN:
            if sys.version.startswith('3.8'):
                # Using new feature from python 3.8
                for location in self.locations:
                    if (num := location.handle_pos(event.pos)):
                        break
            else:
                # If there is an older version of python
                num = 0
                for location in self.locations:
                    n = location.handle_pos(event.pos)
                    if n:
                        num = n
                        break
            if num in self.graph.get(self.location, tuple()):
                self.data['view'] = 'game'
                self.data['position']['location'] = num
                return self.data
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                self.data['view'] = 'game'
                return self.data
        return False
    
    def show(self):
        while True:
            for event in pg.event.get():
                n = self.handle_event(event)
                if n:
                    return n
            self.surface.fill((0, 0, 0))
            self.locations.draw(self.surface)
            pg.display.flip()