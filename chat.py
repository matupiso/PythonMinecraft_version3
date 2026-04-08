from settings import *
import pygame as pg
import moderngl as mgl
import glm
import numpy as np




class Chat:
    def __init__(self, app):
        self.app = app
        self.font = pg.font.Font("freesansbold.ttf", 17)
        self.render_list = []
        self.counter = 0
        self.on = False
        self.pending_messadge = ""


    

    @property
    def on(self):
        return not self.app.player.on
    
    @on.setter
    def on(self, x):
        self.app.player.on = not x

    
    def update(self):
        if self.counter == 600:
            self.counter = 0
            if len(self.render_list) > 0:self.render_list.pop()

        self.counter += 1


    

    def handle_input(self, event:pg.event.Event):
        key = pg.key.get_pressed()
        if key[pg.K_LCTRL] and self.on:
            self.on = False
            if self.pending_messadge.startswith("/"):
                self.chat_command(self.pending_messadge)
            else:
                self.add_messadge("player", self.pending_messadge)
            self.pending_messadge = ""
            return 

        if self.on:
            if key[pg.K_BACKSPACE]:
                self.pending_messadge = self.pending_messadge[:-1] if len(self.pending_messadge) != 0 else ""
            elif event.type == pg.KEYDOWN and event.key < 127:
                self.pending_messadge += event.unicode
        
    def render(self):
        for key, item in enumerate(self.render_list):
            text, color = item
            self.render_at_index(key + 1, text, color)

        if self.on:   self.render_at_index(0, self.pending_messadge + "_")


    def chat_command(self, chat_input):
        if len(chat_input) < 2: return
        chat_input = chat_input[1:]

        level = 2
        

        self.app.commands.execute(chat_input, self.app.player.as_entity(), self.app.player.position, level)
    def add_messadge(self, owner, messadge, color="white"):
        actual_messadge = (f"[{owner}]: {messadge}", color)
        self.render_list.append(actual_messadge)
        



    def render_at_index(self, index, text, color="white"):
        self.render_text(text, (0.09999, WIN_RES.y - 0.099 - (self.font.get_linesize() + 3) * (index + 1)), color=color)


    def render_text(self, text, position, color="white"):
        
        text_surface = self.font.render(text, False, color, "black")
        self.app.scene.render_on_screen(text_surface, *position)



