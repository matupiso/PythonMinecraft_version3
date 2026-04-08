from settings import *
from meshes.chunk_mesh_builder import get_index, get_chunk_index, build_chunk_mesh_special, build_chunk_mesh
from meshes.chunk_mesh import ChunkMesh, ComplicatedChunkMesh
from world_objects.entity import *
from terrian_gen import *
from save import chunk_is_generated, load_chunk

class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.voxels: np.array = None
        x,y, z = position
        self.light_map = np.ones(CHUNK_VOL, dtype='uint8')
        self.mesh:ChunkMesh = None
        self.other_mesh:ComplicatedChunkMesh = None
        self.m_model = self.get_model_matrix()
        self.is_empty = True
        self.is_full = False


        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
    

        
    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    def is_on_frustom(self):
        return self.app.player.frustom.is_on_frustum(self)
    def set_uniform(self):
        self.mesh.program['model'].write(self.m_model)
        self.mesh.program['sun_light'].write(glm.vec3(1, 1, 1))

        self.other_mesh.program['model'].write(self.m_model)
    def build_mesh(self):
        self.mesh = ChunkMesh(self)
        self.other_mesh = ComplicatedChunkMesh(self)
        
        print_info(f"state: chunk_{self.position}_mesh_builded")

    def render(self):
        if not self.is_empty and self.is_on_frustom() and self.is_active and self.mesh:
            self.set_uniform()
            self.mesh.render1()
            #self.other_mesh.render()

    def render_t(self):
         if not self.is_empty and self.is_on_frustom() and self.is_active and self.mesh:
            self.set_uniform()
            self.mesh.render2()
            #self.other_mesh.render()

    @property
    def is_active(self):
        position = glm.ivec3(self.position)

        p1 = position + glm.ivec3(1, 0, 0)
        p2 = position + glm.ivec3(-1, 0, 0)
        p3 = position + glm.ivec3(0, 1, 0)
        p4 = position + glm.ivec3(0, -1, 0)
        p5 = position + glm.ivec3(0, 0, 1)
        p6 = position + glm.ivec3(0, 0, -1)

        adj_chunk1 = self.world.chunks[get_chunk_index(p1)] if get_chunk_index(p1) != -1 else None
        adj_chunk2 = self.world.chunks[get_chunk_index(p2)] if get_chunk_index(p2) != -1 else None
        adj_chunk3 = self.world.chunks[get_chunk_index(p3)] if get_chunk_index(p3) != -1 else None
        adj_chunk4 = self.world.chunks[get_chunk_index(p4)] if get_chunk_index(p4) != -1 else None
        adj_chunk5 = self.world.chunks[get_chunk_index(p5)] if get_chunk_index(p5) != -1 else None
        adj_chunk6 = self.world.chunks[get_chunk_index(p6)] if get_chunk_index(p6) != -1 else None

        adj_chunks = []
        if adj_chunk1: adj_chunks.append(adj_chunk1)
        if adj_chunk2: adj_chunks.append(adj_chunk2)
        if adj_chunk3: adj_chunks.append(adj_chunk3)
        if adj_chunk4: adj_chunks.append(adj_chunk4)
        if adj_chunk5: adj_chunks.append(adj_chunk5)
        if adj_chunk6: adj_chunks.append(adj_chunk6)

        if len(adj_chunks) != 6: return True

        f_count = 0

        for chunk in adj_chunks:
            if chunk.is_full: f_count += 1

        if f_count == 6:
            return False


        return True
        
        
    @staticmethod
    @njit
    def _build_voxels(position):
        #empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype = 'uint8')


        
        #fill the chunk
        cx, cy, cz = position
        cx *= CHUNK_SIZE
        cy *= CHUNK_SIZE
        cz *= CHUNK_SIZE



        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx
                wz = z + cz
                world_height = get_height(wx, wz) 
                if world_height < SEA_LEVEL: world_height = SEA_LEVEL
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = cy + y
                    set_voxel_id(voxels, x, y, z, wx, wy, wz)
             
    

        is_empty = True
        is_full = False
        
        if np.any(voxels):
            is_empty = False
        if np.all(voxels):
            is_full = True


        
        return voxels, is_empty, is_full
    
    def build_voxels(self):
        if GENERATE_OR_LOAD_WORLD == GENERATE or (not chunk_is_generated(self.app.world_name, self.position) and GENERATE_OR_LOAD_WORLD == LOAD):
            voxels, self.is_empty, self.is_full = self._build_voxels(self.position)
            print_info(f"state: chunk_{self.position}_voxels_builded")
        elif GENERATE_OR_LOAD_WORLD == LOAD and chunk_is_generated(self.app.world_name, self.position):
            voxels = load_chunk(self.app.world_name, self.position)
            print_info(f"state: chunk_{self.position}_voxels_loaded")
        
        
        return voxels
    
    def update(self):
        self.is_empty = not np.any(self.voxels)
        self.is_full = np.all(self.voxels)

        if TORCH in self.voxels:
            self.other_mesh = ComplicatedChunkMesh(self)



