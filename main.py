from settings import *
from shader_program import ShaderProgram
from scene import Scene
from voxel_handler import VoxelHandler
from player import Player
from textures import Textures
from collisions import Collisions
from commands import Commands   
from chat import Chat
from terrian_gen import get_height
from sound import Sound
from entity_handler import EntityHandler
import moderngl as mgl          
import pygame as pg
import sys
import light        
from save import save_world, world_exists, load_player, get_seed
from event_handler import EventHandler
import time


class VoxelEngine:
    def __init__(self):
          #initialize pygame and moderngl context
        pg.init()   
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_BUFFER_SIZE, 24)

        #create pygame display
    
        pg.display.set_mode((WIN_RES.x, WIN_RES.y), flags = pg.OPENGL | pg.DOUBLEBUF)

        #grab and devisible the mouse
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    

        #moderngl context
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND) 
        self.ctx.gc_mode = 'auto'

        #clock and timers
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.timer = time.time()

    
        #running flag   
        self.is_running = False

        #sky
        self.sky_color = BG_COLOR   
        self.world_name = input("world name> ") if GENERATE_OR_LOAD_WORLD == LOAD else "???s"
        if GENERATE_OR_LOAD_WORLD == LOAD:

            import settings as st
            if not world_exists(self.world_name):
                st.SEED = int(input("new seed> "))
                
            else:
                st.SEED = get_seed(self.world_name)
            del st
                



        



        #initialize needed objects
        self.on_init()
    def on_init(self):
        
        self.collisions = Collisions(self)
        self.textures = Textures(self)
        
        self.player = Player(self)
        if world_exists(self.world_name) and GENERATE_OR_LOAD_WORLD == LOAD:
            load_player(self.world_name, self.player)

        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)    
        self.voxel_handler = VoxelHandler(self.scene.world)
        self.commands = Commands(self)
        self.chat = Chat(self)              
        self.sound = Sound(self)
        self.entity_handler = EntityHandler(self)
        self.event_handler = EventHandler(self)
    


        

       
        
        

        


        self.sound.set_volume(0.5)
        self.player.position.y = get_height(self.player.position.x,self.player.position.z) + 2

        

    def update(self):
        #update time variables
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001

        #update other things
        self.chat.update()
        self.entity_handler.update()
        self.player.update()    
        self.shader_program.update()
        self.voxel_handler.update()
        self.scene.update()    
   
        self.chat.update() 
        self.event_handler.update( )

    


        #debug
        if DEBUG_MODE:  
            print(f"player: {self.player.position}")

 

        #display current framerate
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')

    def render(self):
        #clear the display
        if self.player.position.y < 0:  
            self.sky_color = glm.vec3(0, 0, 0)


        


        
        self.ctx.clear(color=self.sky_color)

        #render
        self.chat.render() 
        self.scene.render()
        
    
    

        #draw new frame     
        pg.display.flip()
    def handle_events(self):         
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False


            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                print(self.player.position)

            self.chat.handle_input(event)

                

            if event.type == pg.KEYDOWN and event.key == pg.K_t and self.chat.on == False:
                self.chat.on = True

      
            

      
    def run(self):
        self.is_running = True
        while self.is_running:

            self.update()
            self.render()
            self.handle_events()

        if GENERATE_OR_LOAD_WORLD == LOAD:
            save_world(self.world_name, self.scene.world)
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    app = VoxelEngine()
    app.run()