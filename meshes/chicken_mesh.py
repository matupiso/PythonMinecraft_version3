from settings import *
from meshes.base_mesh import BaseMesh, load_model


class ChickenMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chicken

        self.vbo_format = '3f'
        self.attrs = ('in_position',)
        self.vao = None
        self.model = load_model("chicken")
        self.yaw = 0
        self.red = False
        self.pitch = 0


        self.position = PLAYER_START_POS + glm.vec3(0, 10, 0)
        

    def render(self):
        self.vao = self.get_vao()
        super().render()

    def set_uniform(self):

        model_mat = glm.rotate(glm.translate(glm.mat4(), self.position), glm.radians(self.yaw), glm.vec3(0, 1, 0))
        model_mat = glm.rotate(model_mat, glm.radians(self.pitch), glm.vec3(0, 0, 1))
        self.program['model'].write(model_mat)
        self.program['view'].write(self.app.player.m_view)
        self.program['color'] = glm.vec3(1, 0.4, 0.4) if self.red else glm.vec3(1,1,1)
        



  

    def get_vertex_data(self):
        return self.model