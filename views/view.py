import pygame as pg

from server import handler


def exit_game(data):
    print(data)
    payload = {
        'account': {
            'login': data['account'].split()[0],
            'password': data['account'].split()[1]
        },
        'position': data['position']
    }
    res = handler.get_json_response('exit/', data=payload)
    print(res)


class View:

    def __init__(self, surface, data):
        self.surface = surface
        self.data = data
    
    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    def show(self):
        while True:
            for event in pg.event.get():
                self.handle_event(event)

            self.surface.fil((0, 0, 0))

            pg.display.flip()