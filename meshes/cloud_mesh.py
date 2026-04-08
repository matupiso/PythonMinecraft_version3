from settings import *
from meshes.base_mesh import BaseMesh
from noise import *


class CloudMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.ctx = self.app.ctx
        self.program = self.app.shader_program.clouds
        self.vbo_format = '3u2'
        self.attrs = ('in_position',)
        self.vao = self.get_vao()

    def get_vertex_data(self):
        data = np.array([
             0.0, CLOUD_HEIGHT, 0.0,
             WORLD_W * CHUNK_SIZE, CLOUD_HEIGHT, WORLD_D * CHUNK_SIZE,
             WORLD_W * CHUNK_SIZE, CLOUD_HEIGHT, 0.0,
             0.0, CLOUD_HEIGHT, 0.0,
             0.0, CLOUD_HEIGHT, WORLD_D * CHUNK_SIZE,
             WORLD_W * CHUNK_SIZE, CLOUD_HEIGHT, WORLD_D * CHUNK_SIZE, 
        ], dtype="float32")

        return data