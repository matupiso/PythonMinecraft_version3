from settings import *


class ShaderProgram:
    def __init__(self, app):
        #wee will need the main application and moderngl context
        self.app = app
        self.ctx = app.ctx

        #-----------shaders-------------#
        self.chunk = self.get_program('chunk')
        self.marker = self.get_program('marker')
        self.sun = self.get_program('sun')
        self.clouds = self.get_program("clouds")
        self.complicated_chunk = self.get_program("complicated_chunk")
        self.gui = self.get_program("gui")
        self.chicken = self.get_program("chicken")
        #-------------------------------#

        #set shader uniforms 
        self.set_uniforms_on_init()


        print_info("state: shader_initialized")

    def set_uniforms_on_init(self):
        self.chunk['model'].write(glm.mat4())
        self.chunk['proj'].write(self.app.player.m_proj)
        self.chunk['u_texture_array_0'] = 1
        self.chunk['block_breaking_array'] = 12
        
        self.chunk['bg_color']  = glm.vec3(self.app.sky_color.xyz)


        self.complicated_chunk['model'].write(glm.mat4())
        self.complicated_chunk['proj'].write(self.app.player.m_proj)
        self.complicated_chunk['torch_top'] = 4
        self.complicated_chunk['torch_side'] = 3
        self.complicated_chunk['tf_1'] = 6
        self.complicated_chunk['tf_2'] = 7
        self.complicated_chunk['tf_3'] = 8
        self.complicated_chunk['tf_4'] = 9
        self.complicated_chunk['tf_5'] = 10
        self.complicated_chunk['tf_6'] = 11
        self.complicated_chunk['glass_side'] = 13
        

        self.gui['image'] = 14
       

        self.marker['proj'].write(self.app.player.m_proj)
        self.marker['model'].write(glm.mat4())
        self.marker['u_texture_0'] = 0

        self.sun['proj'].write(self.app.player.m_proj)
        self.sun['model'].write(glm.mat4())
        self.sun['u_texture_0'] = 2

      

        self.clouds["m_proj"].write(self.app.player.m_proj)

        self.chicken['proj'].write(self.app.player.m_proj)
        self.chicken['model'].write(glm.mat4())

        

    def update(self):
        self.chunk['view'].write(self.app.player.m_view)
        self.chunk['bg_color']  = glm.vec3(self.app.sky_color.xyz)

        self.complicated_chunk['view'].write(self.app.player.m_view)
        

    
        self.marker['view'].write(self.app.player.m_view)
        self.sun['view'].write(self.app.player.m_view)
        self.clouds['m_view'].write(self.app.player.m_view)
        self.chicken['view'].write(self.app.player.m_view)
        self.gui['water_screen'] = glm.vec2(1, 0.4) if self.app.player.water_live_seconds > 7 else glm.vec2(1, 0.7)
      
      
    
        
        

        

    def get_program(self, name):

        #get shaders
        with open(f"shaders\\{name}.frag") as file:
            fragment_shader = file.read()

        with open(f"shaders\\{name}.vert") as file:
            vertex_shader = file.read()
        
        #create shader program object using ctx 
        program = self.ctx.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        
        #return the program
        return program
