from views import map

# It would be good to use python 3.8.1 and the latest pygame 2.0.0dev6
import pygame

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
# current_window = main.MainView(screen)
# location = current_window.show()
current_window = map.Map(screen, 4)
location = current_window.show()
print(location)
