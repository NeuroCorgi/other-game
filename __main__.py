import pygame

pygame.init()

screen = pygame.display.set_mode(pygame.FULLSCRENN)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
