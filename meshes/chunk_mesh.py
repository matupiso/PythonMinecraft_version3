from meshes.base_mesh import BaseMesh, MixedBaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh, build_chunk_mesh_special, get_index
from settings import *


class ChunkMesh(MixedBaseMesh):
    ATTRS = ("in_position", "voxel_id", "face_id", "ao_id", "light_id", "crack_id")
    VBO_FORMAT = "3u1 1u1 1u1 1u1 1u1 1u1"
    FORMAT_SIZE = sum(int(fmt[:1]) for fmt in VBO_FORMAT.split())
    def __init__(self, chunk):
        super().__init__()

        self.voxels = chunk.voxels
        self.chunk = chunk
        self.ctx = chunk.app.ctx
        self.attrs = self.ATTRS
        self.vbo_format = self.VBO_FORMAT
        self.format_size = self.FORMAT_SIZE
        self.app = chunk.app
        self.program = chunk.app.shader_program.chunk
        self.vao1 = self.get_vao1()
        self.vao2 = self.get_vao2()
        

    def get_vertex_data1(self):
        return build_chunk_mesh(
            chunk_voxels=self.voxels,
            format_size=self.format_size,
            chunk_position=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
            light_map=np.array(np.multiply(self.chunk.light_map, 100), dtype="uint8") ,
            crack_pos=tuple(self.chunk.world.crack_pos) if self.chunk.world.crack_pos else None,
            crack_index=self.chunk.world.acrack_index if self.chunk.world.crack_pos else 6,
            transparent_mesh = False
       )
    def get_vertex_data2(self):
        return build_chunk_mesh(
            chunk_voxels=self.voxels,
            format_size=self.format_size,
            chunk_position=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
            light_map=np.array(np.multiply(self.chunk.light_map, 100), dtype="uint8") ,
            crack_pos=tuple(self.chunk.world.crack_pos) if self.chunk.world.crack_pos else None,
            crack_index=self.chunk.world.acrack_index if self.chunk.world.crack_pos else 6,
            transparent_mesh = True
       )
    

    

class ComplicatedChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()

        self.voxels = chunk.voxels
        self.chunk = chunk
        self.ctx = chunk.app.ctx
        self.app = chunk.app
        self.attrs = ("in_position", "tex_type", "in_uv")
        self.vbo_format = "3f 1f 2f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.program = chunk.app.shader_program.complicated_chunk
        self.vao = self.get_vao() if TORCH in self.voxels or GLASS in self.voxels else None
       

                        

    def render(self):
        if self.vao: super().render()

    def get_vertex_data(self):
        return build_chunk_mesh_special(
            chunk_voxels=self.voxels,
            format_size=self.format_size,
            torch_index = self.chunk.world.torch_index

        )