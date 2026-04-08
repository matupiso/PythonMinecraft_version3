from settings import *
from meshes.base_mesh import BaseMesh


class CubeMesh(BaseMesh):
    def __init__(self, app, shader):
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = shader
        self.active = False
        self.position = glm.vec3(0, 0, 0)
        self.size = glm.vec3(1, 1, 1)

        self.vbo_format = '2f2 3f2'
        self.attrs = ('in_tex_coord_0', 'in_position',)
        self.vao = None



    def render(self):
        if self.active:
            super().render()

    def set_uniform(self):
        self.program['model'].write(glm.translate(glm.mat4(), glm.vec3(self.position)))

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='float16')

    def get_vertex_data(self):
        x,y,z = self.size
        x0 = (1 - x) / 2
        x1 = 1 - x0
        z0 = (1 - z) / 2
        z1 = 1 - z0

        

        vertices = [
            (x0, 0, z1), (x1, 0, z1), (x1, y, z1), (x0, y, z1),
            (x0, y, z0), (x0, 0, z0), (x1, 0, z0), (x1, y, z0)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data



















