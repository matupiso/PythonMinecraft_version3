from settings import *
from meshes.cloud_mesh import CloudMesh


class Clouds:
    def __init__(self, app):
        self.app = app
        self.mesh = CloudMesh(app)

    def update(self):
        pass

    def render(self):
        self.mesh.render()
