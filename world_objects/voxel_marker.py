from settings import *
from meshes.cube_mesh import CubeMesh
from utils import get_block_size


class VoxelMarker:
    def __init__(self, app):
        self.mesh = CubeMesh(app, app.shader_program.marker)
        self.mesh.vao = self.mesh.get_vao()
        self.app = app

    def update(self):
        pass


    def render(self):
        
        if self.app.voxel_handler.voxel_world_pos and not self.app.voxel_handler.entity:
            self.mesh.position = self.app.voxel_handler.voxel_world_pos
            self.mesh.active = True
            if not self.mesh.size == get_block_size(self.app.voxel_handler.voxel_id):
                self.mesh = CubeMesh(self.app, self.app.shader_program.marker)
                self.mesh.size = get_block_size(self.app.voxel_handler.voxel_id)
                self.mesh.vao = self.mesh.get_vao()
                


        else:
            self.mesh.active = False
        self.mesh.set_uniform()

        self.mesh.render()
        