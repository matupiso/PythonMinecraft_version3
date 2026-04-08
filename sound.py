import pygame as pg
from typing import Union, Literal
import time
from settings import *
from utils import get_distance

_volume_type = Union[float, Literal['not_assigned',]]



class Sound:
    def __init__(self, app):
        self.current_sound = None
        self.volume = None
        self.t = 0
        self.app = app
        self.can_play = True
    def    set_volume(self, volume:_volume_type):
        if volume == "not_assigned": self.volume = None
        else:self.volume = volume
    def update(self):
        if self.t >= time.time():
            self.can_play = True
    def playsound(self, indicator:str, volume=0.4):
        location1 = f"assets\\sounds\\{indicator.replace(".", "\\")}.wav"
        location2 = f"assets\\sounds\\{indicator.replace(".", "\\")}.mp3"

        try:
            if self.can_play:
                self.current_sound  = pg.mixer.Sound(location1)
                self.current_sound.set_volume(volume)
                self.t = time.time() + self.current_sound.get_length()
                self.current_sound.play()
                
            return True
        
        except:
            try:
                if self.can_play:
                    self.current_sound = pg.mixer.Sound(location2)
                    self.current_sound.set_volume(volume)
                    self.t = time.time() + self.current_sound.get_length()
                    self.current_sound.play()
                return True
            
            except: return False
    
    def playsound_localy(self, indicator, sound_emit_position):
        distance = get_distance(self.app.player.position, sound_emit_position)
        if distance > PLAYER_MAX_SOUND_DISTANCE:
            return False
        distance /= PLAYER_MAX_SOUND_DISTANCE
        distance = 1 - distance
        volume = distance * 0.3
        return self.playsound(indicator, volume=volume)



