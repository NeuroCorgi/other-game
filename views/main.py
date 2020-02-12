# View for login page
import os

from server import handler

from views.view import View, exit_game

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


class MainView(View):
    # background = load_image('login.png')

    def __init__(self, surface, data):
        super().__init__(surface, data)

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

        # Main box
        pg.draw.rect(self.surface, (100, 255, 100), (60, 240, 450, 230), 3)
        
        # Buttons
        self.login_button = font.render("Login", 3, self.login_button_color)
        self.surface.blit(self.login_button, (90, 250))

        self.register_button = font.render("Register", 3, self.register_button_color)
        self.surface.blit(self.register_button, (310, 250))

        # Error box
        message_box = font.render(self.message, 1, (Color('blue1')))
        self.surface.blit(message_box, (80, 100))

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

        # Exit button
        self.exit_box = pg.draw.rect(self.surface, Color('cyan'), (80, 970, 200, 45), 2)
        exit_button = font.render("Exit", 2, Color('cyan'))
        self.surface.blit(exit_button, (90, 980))

    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.MOUSEBUTTONDOWN:

            if self.exit_box.collidepoint(event.pos):
                pg.quit()
                exit(0)

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

        elif event.type == pg.KEYDOWN:
            if self.active_field == 1:
                if event.key == pg.K_RETURN:
                    self.login_done = True
                    if not self.password_done:
                        self.active_field = 2
                        self.login_color = self.notactive_color
                        self.password_color = self.active_color
                elif event.key == pg.K_BACKSPACE:
                    self.login = self.login[:-1]
                else:
                    self.login += event.unicode
            elif self.active_field == 2:
                if event.key == pg.K_RETURN:
                    self.password_done = True
                    if not self.login_done:
                        self.active_field = 1
                        self.login_color = self.active_color
                        self.password_color = self.notactive_color
                elif event.key == pg.K_BACKSPACE:
                    self.password = self.login[:-1]
                else:
                    self.password += event.unicode
    
    def show(self):
        while True:
            for event in pg.event.get():
                self.handle_event(event)

            if self.login_done and self.password_done:
                url = 'enter/' if self.active_button == 1 else 'register/'
                payload = {'account': {'login': self.login, 'password': self.password}}
                res = handler.get_json_response(url, payload)
                if type(res) is not dict and self.active_button == 1:
                    self.login = self.password = ''
                    self.login_done = self.password_done = False
                    self.message = 'Такого пользователя не существует'
                else:
                    if self.active_button == 1 or res['is_free']:
                        if self.active_button == 2:
                            self.data['view'] = 'intro'
                        else:
                            self.data['view'] = 'game'
                        self.data['account'] = self.login + ' ' + self.password
                        self.data['position']['location'] = res['location']['num']
                        self.data['position']['coords'] = res['location']['coords']
                        return self.data
                    else:
                        self.login = self.password = ''
                        self.login_done = self.password_done = False
                        self.message = 'Такой пользователь уже сущетсвует'
                     
            self.surface.fill((0, 0, 0))
            self.draw()
            pg.display.flip()


class PauseView(View):
    
    def draw(self):
        font = pg.font.Font(None, 70)

        # Continue button
        self.continue_box = pg.draw.rect(self.surface, Color('cyan'), (1070, 210, 200, 45), 2)
        continue_button = font.render("Continue", 2, Color('cyan'))
        self.surface.blit(continue_button, (1080, 220))

        # Log out button
        self.logout_box = pg.draw.rect(self.surface, Color('cyan'), (1070, 410, 200, 45), 2)
        logout_button = font.render("Log Out", 2, Color('cyan'))
        self.surface.blit(logout_button, (1080, 420))

        # Exit button
        self.exit_box = pg.draw.rect(self.surface, Color('cyan'), (1070, 610, 200, 45), 2)
        exit_button = font.render("Exit", 2, Color('cyan'))
        self.surface.blit(exit_button, (1080, 620))
    
    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN:
            
            if self.continue_box.collidepoint(event.pos):
                # Return game view
                return 'g'
            elif self.logout_box.collidepoint(event.pos):
                # Return main view with login/register
                exit_game(self.data)
                return 'm'
            elif self.exit_box.collidepoint(event.pos):
                exit_game(self.data)
                pg.quit()
                exit(0)

    def show(self):
        while True:
            acts = {self.handle_event(event) for event in pg.event.get()}
            if any(acts):
                if 'g' in acts:
                    self.data['view'] = 'game'
                elif 'm' in acts:
                    self.data['view'] = 'main'
                return self.data
            self.surface.fill((0, 0, 0))
            self.draw()

            pg.display.flip()


class StoryView(View):

    def __init__(self, surface, data, education=True, *phrases):
        super().__init__(surface, data)
        if education:
            with open('education') as f:
                self.stages = f.read().split('\n\n')
        else:
            self.stages = phrases
        self.last = len(self.stages)

        self.stage = 0

    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

        if event.type == pg.KEYDOWN:
            self.stage += 1
    
    def show(self):
        while True:
            for event in pg.event.get():
                self.handle_event(event)
            
            if self.stage == self.last:
                self.data['view'] = 'game'
                return self.data

            self.surface.fill((0, 0, 0))
            
            font = pg.font.Font(None, 50)

            lines = self.stages[self.stage].split('\n')
            i = 40
            for line in lines:
                text = font.render(line, 1, Color('green'))
                self.surface.blit(text, (40, i))
                i += text.get_height() + 5

            pg.display.flip()
    

class ErrorWindow(View):
    
    def __init__(self, surface, message):
        super().__init__(surface)

        font = pg.font.Font(None, 50)

        self.surface.blit(font.render(message, 1, Color('lightblue')), (100, 60))

        self.surface.blit(font.render('Press "R" to retry', 3, Color('green')), (110, 100))
    
    def show(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        return
            self.surface.fill((0, 0, 0))

            pg.display.flip()