from settings import *
from world_objects.chunk import Chunk
from frustom import chunk_in_reach
from meshes.chunk_mesh_builder import get_chunk_index, get_index
from utils import get_light, numpyindex, get_xyz, get_distance


class ImitatorChunk:
    def __init__(self, x, y, z):
        self.center = (glm.vec3(x, y, z) + 0.5) * CHUNK_SIZE

class World:
    def __init__(self, app):
        self.app = app
        self.tg_timer = 0
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype="uint8")
        self.torch_index = 0
        self.crack_pos:glm.ivec3 = None
        self.acrack_index:int = None


        # self.build_chunks()
        # self.build_chunk_mesh()
        # self.light(self.voxels, self.light_map)

        print_info("state: world_initialized")

    def build_chunk(self, x, y, z):
 
        chunk = Chunk(self, position = (x, y, z))

        chunk_index = int(x + WORLD_W * z + WORLD_AREA * y)
        self.chunks[chunk_index] = chunk

        self.voxels[chunk_index] = chunk.build_voxels()
        

        chunk.voxels = self.voxels[chunk_index]

        chunk.build_mesh()


    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position = (x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    self.voxels[chunk_index] = chunk.build_voxels()
                    

                    chunk.voxels = self.voxels[chunk_index]

    def render(self):
        # if self.tg_timer >= 400:
        #     chunks_builded = 0
        #     for x in range(WORLD_W):
        #         for y in range(WORLD_H):
        #             for z in range(WORLD_D):
        #                 chunk_index = x + WORLD_W * z + WORLD_AREA * y
        #                 if self.app.player.frustom.is_on_frustum(ImitatorChunk(x, y, z)):
        #                     chunk = self.chunks[chunk_index]
        #                     if not chunk and chunks_builded < 1:
        #                         self.build_chunk(x, y, z)
        #                         chunks_builded += 1
        #                     chunk = self.chunks[chunk_index]
                            
        #                     if chunk: chunk.render()   

        #     self.corr = False       
        #     self.tg_timer = 0
        # else:
        #     self.tg_timer += 1

        
        
        for chunk in list(filter(lambda c: bool(c), self.chunks)):
            if self.app.player.frustom.is_on_frustum(chunk):
                chunk.render()     
        for chunk in list(filter(lambda c: bool(c), self.chunks)):
            if self.app.player.frustom.is_on_frustum(chunk):
                chunk.render_t()        




    def update(self):
        for chunk in filter(lambda c: bool(c), self.chunks):
               
            if self.app.player.frustom.is_on_frustum(chunk):
                chunk.update()
        x = random.randint(-4, 4) * CHUNK_SIZE + int(self.app.player.position.x)
        y = random.randint(-4, 4) * CHUNK_SIZE + int(self.app.player.position.y)
        z = random.randint(-4, 4) * CHUNK_SIZE + int(self.app.player.position.z)
        chunk_index = get_chunk_index((x, y, z))
        if not chunk_index == -1 and not self.chunks[chunk_index]:
            self.build_chunk(x // CHUNK_SIZE, y // CHUNK_SIZE, z // CHUNK_SIZE)

        

        self.torch_index += 1
        self.torch_index %= 6




        

      
    # @staticmethod
    # @njit
    # def light(world_voxels, world_light_map):
    #     light_map = np.zeros(np.shape(world_voxels))
    #     for wx in range(WORLD_W):
    #         for wy in range(WORLD_H):
    #             for wz in range(WORLD_D):
    #                 chunk_index = get_chunk_index((wx,wy,wz))
    #                 for x in range(WORLD_W):
    #                     for y in range(WORLD_H):
    #                         for z in range(WORLD_D):    
    #                             index = get_index(x, y, z)
    #                             block = world_voxels[chunk_index][index]
    #                             if is_light(block):
    #                                 emit_light(world_voxels,light_map,(wx * CHUNK_SIZE + x, wy * CHUNK_SIZE + y, wz * CHUNK_SIZE + z), BLOCK_LIGHT)
    #     world_light_map = light_map.data

            
        


