# View for login page
import os

from server import RequestsHandler

import pygame as pg
from pygame import Color


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


class MainView:
    # background = load_image('login.png')

    def __init__(self, surface):
        self.surface = surface

        self.active_color = Color('dodgerblue2')
        self.notactive_color = Color('lightskyblue3')

        # Buttons properties
        self.active_button = 1
        self.login_button_color = self.active_color
        self.register_button_color = self.notactive_color

        # Input fields properties
        self.login = self.password = self.message = ''
        self.login_done = self.password_done = False
        self.login_color = self.password_color = self.notactive_color
        self.active_field = 0
    
    def draw(self):
        font = pg.font.Font(None, 50)

        name = font.render("Game Name", 1, Color('lightblue'))
        self.surface.blit(name, (100, 60))

        # Login box
        pg.draw.rect(self.surface, (100, 255, 100), (60, 240, 450, 230), 3)
        
        # Buttons
        self.login_button = font.render("Login", 3, self.login_button_color)
        self.surface.blit(self.login_button, (90, 250))

        self.register_button = font.render("Register", 3, self.register_button_color)
        self.surface.blit(self.register_button, (310, 250))

        # Error box
        message_box = font.render(self.message, 1, (Color('blue1')))
        self.surface.blit(message_box, (80, 3100))

        # Labels
        login = font.render("login", 3, (100, 255, 100))
        self.surface.blit(login, (80, 360))

        password = font.render("password", 3, (100, 255, 100))
        self.surface.blit(password, (80, 420))

        # Input fields
        self.login_input_box = pg.draw.rect(self.surface, self.login_color, (290, 350, 200, 45), 2)
        self.login_input = font.render(self.login, 2, (255, 255, 255))
        self.surface.blit(self.login_input, (300, 360))

        self.password_input_box = pg.draw.rect(self.surface, self.password_color, (290, 410, 200, 45), 2)
        self.password_input = font.render(self.password, 2, (255, 255, 255))
        self.surface.blit(self.password_input, (300, 420))

    def get_action(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.MOUSEBUTTONDOWN:

            if self.login_button.get_rect().move(90, 250).collidepoint(event.pos):
                self.active_button = 1
                self.login_button_color = self.active_color
                self.register_button_color = self.notactive_color

            elif self.register_button.get_rect().move(310, 250).collidepoint(event.pos):
                self.active_button = 2
                self.login_button_color = self.notactive_color
                self.register_button_color = self.active_color

            if self.login_input_box.collidepoint(event.pos):
                self.active_field = 1
                self.login_color = self.active_color
                self.password_color = self.notactive_color

            elif self.password_input_box.collidepoint(event.pos):
                self.active_field = 2
                self.login_color = self.notactive_color
                self.password_color = self.active_color

            else:
                self.active_field = 0
                self.login_color = self.password_color = self.notactive_color                

        if event.type == pg.KEYDOWN:
            if self.active_field == 1:
                if event.key == pg.K_RETURN:
                    self.login_done = True
                elif event.key == pg.K_BACKSPACE:
                    self.login = self.login[:-1]
                else:
                    self.login += event.unicode
            if self.active_field == 2:
                if event.key == pg.K_RETURN:
                    self.password_done = True
                elif event.key == pg.K_BACKSPACE:
                    self.password = self.login[:-1]
                else:
                    self.password += event.unicode
    
    def show(self):
        while True:
            for event in pg.event.get():
                self.get_action(event)

            if self.login_done and self.password_done:
                url = 'login/' if self.active_button == 1 else 'register/'
                data = {'account': self.login + ' ' + self.password}
                res = RequestsHandler.get_json_response(url, data)
                if not res:
                    self.login = self.password = ''
                    self.login_done = self.password_done = False
                    self.message = 'Такого пользователя не существует'
                else:
                    if self.active_button == 1 or res['is_free']:
                        return res['location']
                    else:
                        self.message = 'Такой пользователь уже сущетсвует'
                     
            self.surface.fill((0, 0, 0))
            self.draw()
            pg.display.flip()
