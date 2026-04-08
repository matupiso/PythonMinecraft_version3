from settings import *
from world_objects.world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.sun import Sun
from world_objects.clouds import Clouds
from moderngl import DEPTH_TEST
import pygame as pg


class Scene:
    def __init__(self, app):
        #create application instance
        self.app = app

        

        #rendering objects
        self.world = World(app)
        self.marker = VoxelMarker(app)
        self.sun = Sun(app)
        self.clouds = Clouds(app)
        self.on_screen_image = pg.surface.Surface((WIN_RES.x, WIN_RES.y))
        self.on_screen_image.fill("black")
     
        

        print_info("state: scene_initialized")

    def render(self):
        self.app.ctx.enable(DEPTH_TEST)
        #render all rendering objects
        self.sun.render()
        self.world.render()
        self.marker.render()
      
        self.app.entity_handler.render()


        #this rendering is little bit diffrent        
        self.app.player.render()

        self.app.ctx.disable(DEPTH_TEST)
        screen = pg.transform.rotate(self.on_screen_image, -90)
        texture = self.app.textures.load_from_texture(screen, is_tex_array=False, fx=True, fy=False)
        texture.use(location = 14)

    

        vbo = np.array([
            -1, -1, 0,  1, 0,
             1,  1, 0,  0, 1,
            -1,  1, 0,  0, 0,

            -1, -1, 0,  1, 0,
             1,  -1, 0,  1, 1,
             1, 1, 0,  0, 1,

        ], dtype='float32')

        vbo = self.app.ctx.buffer(vbo)

        vao = self.app.ctx.vertex_array(
            self.app.shader_program.gui,
            [(vbo, "3f 2f", "in_pos", "in_uv")], skip_errors = True
        )
        vao.render()

        self.on_screen_image.fill("black")

 
  

    def update(self):
        self.sun.update()
        self.world.update()
        self.marker.update()
        
    def render_on_screen(self, image:pg.surface.Surface, x, y):
        self.on_screen_image.blit(image, (x, y))

        
