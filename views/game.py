# Basic game view
import os
import sys

from itertools import repeat

from views.view import View
from views.main import ErrorWindow
from server import handler

import pygame as pg
clock = pg.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pg.image.load(fullname)
    # if colorkey is not None:
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image


class Ships(pg.sprite.Sprite):
    # Для проекта сойдёт и одна картика, я не дизайнер
    image = load_image('ship_image.png')

    def __init__(self, group, name, coords):
        super().__init__(group)

        self.name = name

        self.image = Ships.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def hover(self, pos):
        if self.rect.collidepoint(pos):
            return (self.name, (self.rect.x + self.rect.width, self.rect.y))
        return ''

    def update(self, name, coords):
        if name == self.name:
            self.rect.x, self.rect.y = coords


class Static:

    def update(self, coords):
        self.rect.x = self.rect.x - coords[0]
        self.rect.y = self.rect.y - coords[1]
    
    def clicked(self, coords, sprite):
        if self.rect.collidepoint(coords) and self.rect.colliderect(sprite.rect):
            return self.number


class Gate(pg.sprite.Sprite, Static):
    # Для проекта сойдёт и одна картика, я не дизайнер
    image = load_image('gate.png')

    def __init__(self, group, num, coords):
        super().__init__(group)
        self.type = 'gate'

        self.number = num
        self.image = Gate.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def update(self, coords):
        self.rect.x -= coords[0]
        self.rect.y -= coords[1]
    
    def hover(self, pos):
        if self.rect.collidepoint(pos):
            return ('gate', (self.rect.x + self.rect.width, self.rect.y))
        return ''


class TradeStation(pg.sprite.Sprite):
    # Для проекта сойдёт и одна картика, я не дизайнер
    image = load_image('trade_station_image.png')

    def __init__(self, group, num, coords):
        super().__init__(group)
        self.type = 't_station'

        self.number = num
        self.image = TradeStation.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def update(self, coords):
        self.rect.x -= coords[0]
        self.rect.y -= coords[1]

    def hover(self, pos):
        if self.rect.collidepoint(pos):
            return ('trade station', (self.rect.x + self.rect.width, self.rect.y))
        return ''


class QuestStation(pg.sprite.Sprite):
    # Для проекта сойдёт и одна картика, я не дизайнер
    image = load_image('quest_station_image.png')

    def __init__(self, group, num, coords):
        super().__init__(group)
        self.type = 'q_station'

        self.number = num
        self.image = QuestStation.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def update(self, coords):
        self.rect.x -= coords[0]
        self.rect.y -= coords[1]

    def hover(self, pos):
        if self.rect.collidepoint(pos):
            return ('quest station', (self.rect.x + self.rect.width, self.rect.y))
        return ''


class Turret(pg.sprite.Sprite):
    image = load_image('turret_image.png')

    def __init__(self, group, num, coords):
        super().__init__(group)
        self.type = 'q_station'

        self.number = num
        self.image = Turret.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
    
    def update(self, coords):
        self.rect.x -= coords[0]
        self.rect.y -= coords[1]

    def hover(self, pos):
        if self.rect.collidepoint(pos):
            return ('turret', (self.rect.x + self.rect.width, self.rect.y))
        return ''


class GameView(View):

    def __init__(self, surface, data):
        super().__init__(surface, data)

        self.moving = [0, 0]

        self.ships = pg.sprite.Group()
        self.static = pg.sprite.Group()

        self.num = data['position']['location']
        self.coords = data['position']['coords']

        self.account = data['account']

        self.players = dict()

        data = {
            'location': {
                'num': self.num,
            },
            'account': self.account,
        }

        objects = handler.get_json_response('objects/', data=data)['objects']
        for object in objects:
            num, type, coords = object
            move = lambda x, y, z: x - y + z

            if type == 'gate':
                Gate(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'trade_station':
                TradeStation(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'quest_station':
                QuestStation(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'turret':
                pass
    
    def jump(self, object):
        self.static = pg.sprite.Group()

        payload = {
            'account': self.account,
            'location': self.num,
            'object': object
        }
        data = handler.get_json_response('jump/gates/', data=payload)
        print(data)
        self.num = data['location']
        for object in data['objects']:
            num, type, coords = object
            move = lambda x, y, z: x - y + z

            if type == 'gate':
                Gate(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'trade_station':
                TradeStation(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'quest_station':
                QuestStation(self.static, num, tuple(map(move, coords, self.coords, (960, 540))))
            elif type == 'turret':
                pass

    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == pg.K_w:
                self.moving[1] = -10
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.moving[1] = 10
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.moving[0] = -10
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.moving[0] = 10

            if event.key == pg.K_m:
                return 'm'
            if event.key == pg.K_ESCAPE:
                return 'e'

        if event.type == pg.KEYUP:
            if (event.key == pg.K_UP or event.key == pg.K_w or 
                    event.key == pg.K_DOWN or event.key == pg.K_s):
                self.moving[1] = 0
            if (event.key == pg.K_LEFT or event.key == pg.K_a or 
                    event.key == pg.K_RIGHT or event.key == pg.K_d):
                self.moving[0] = 0

        if event.type == pg.MOUSEBUTTONDOWN:
            for static in self.static:
                if static.type == 'gate':
                    if sys.version.startswith('3.8'):
                        if (num := static.clicked(pg.mouse.get_pos(), self.players[self.account])):
                            self.jump(num)
                    else:
                        num_ = static.clicked(pg.mouse.get_pos())
                        if num_:
                            self.jump(num_)

    def show(self):
        while True:
            acts = {self.handle_event(event) for event in pg.event.get()}
            if any(acts):
                self.data['position']['location'] = self.num
                self.data['position']['coords'] = self.coords
                if 'm' in acts:
                    self.data['view'] = 'map'
                elif 'e' in acts:
                    self.data['view'] = 'esc'
                return self.data

            self.surface.fill((0, 0, 0))

            time = clock.tick()
            movement = tuple(map(lambda x, y: x * y / 1000, self.moving, repeat(time)))
            self.static.update(movement)
            self.coords = tuple(map(lambda x, y: x + y, self.coords, movement))
            message = 0

            # hover effect
            for static in self.static:
                if sys.version.startswith('3.8'):
                    if (message := static.hover(pg.mouse.get_pos())):
                        break
                else:
                    message_ = static.hover(pg.mouse.get_pos())
                    if message_ != '':
                        message = message_
                        break
            
            if message:
                try:
                    message, (x, y) = message
                    font = pg.font.Font(None, 30)
                    text = font.render(message, 1, (100, 255, 100))
                    self.surface.blit(text, (x, y))
                except ValueError:
                    pass
            
            # get other players coords
            paylod = {
                'account': self.account,
                'location': {
                    'num': self.num,
                    'coords': self.coords
                }
            }

            players = handler.get_json_response('update/', data=paylod)['players']

            # initialize and move players
            move = lambda x, y, z: x - y + z
            for player in players:
                if self.players.get(player['name'], 0):
                    if player['name'] != self.account:
                        self.ships.update(
                            name=player['name'], coords=map(move, player['coords'], self.coords, (960, 540))
                        )
                else:
                    self.players[player['name']] = Ships(
                        self.ships, player['name'], map(move, player['coords'], self.coords, (960, 540))
                    )
            
            # delte players who left location
            for player in set(self.players.keys()) - set(map(lambda x: x['name'], players)):
                self.ships.remove(self.players[player])
                del self.players[player]

            # draw objects
            self.ships.draw(self.surface)
            self.static.draw(self.surface)

            pg.display.flip()
