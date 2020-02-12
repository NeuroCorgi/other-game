from views.main import MainView, StoryView, ErrorWindow, PauseView
from views.map import MapView
from views.game import GameView

from server import handler
# It would be good to use python 3.8.1 and pygame 2.0.0dev6
import pygame

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

if handler.test():
    # current_screen = MainView(screen)
    # location, account, method = current_screen.show()
    # if method == 2:
    #     current_screen = StoryView(screen)
    #     current_screen.show()
    #
    # current_screen = GameView(screen, location['num'], location['coords'], account)

    data = {
        'view': 'main',
        'position': {
            'location': 0,
            'coords': (0, 0)
        },
        'account': ''
    }

    while True:
        if data['view'] == 'game':
            current_screen = GameView(screen, data)
        if data['view'] == 'map':
            current_screen = MapView(screen, data)
        elif data['view'] == 'esc':
            current_screen = PauseView(screen, data)
        elif data['view'] == 'main':
            current_screen = MainView(screen, data)
        elif data['view'] == 'intro':
            current_screen = StoryView(screen, data)
        
        data = current_screen.show()

else:
    current_screen = ErrorWindow(screen, 'Connection failed')
    current_screen.show()
