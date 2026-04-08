from settings import *
from meshes.chunk_mesh_builder import get_chunk_index, get_index
from world_objects.entity import Torch
from numba import uint16

class VoxelHandler:
    def __init__(self, world):
        self.app = world.app
        self.world = world


        #ray cast result
        self.voxel_id = None
        self.voxel_world_pos = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_normal = None
        self.entity = None

       
        print_info("state: voxel_handler_initialized")


    def update(self):
        self.ray_cast()

    #returns voxel id
    def get_block(self, wx, wy, wz):
        chunk_index = (get_chunk_index((wx, wy, wz)))
        if not chunk_index in range(WORLD_VOL):
            return 0, 0, 0, 0
        
        chunk = self.world.chunks[chunk_index]
        if not chunk:
            self.world.build_chunk(wx // CHUNK_SIZE, wy // CHUNK_SIZE, wz // CHUNK_SIZE)

        chunk = self.world.chunks[chunk_index]
        
        cx, cy, cz = chunk.position
        cx *= CHUNK_SIZE
        cy *= CHUNK_SIZE
        cz*= CHUNK_SIZE
        lx, ly, lz = wx - cx, wy - cy, wz - cz

        local_voxel_position = (get_index(lx, ly, lz))

        return chunk.voxels[local_voxel_position], local_voxel_position, (lx, ly, lz), chunk
    def getblock(self, wx, wy, wz): return (self.get_block(wx, wy, wz)[0])
    
    def rebuild_chunk(self, cx, cy, cz):
        chunk_index = (get_chunk_index((cx * CHUNK_SIZE, cy * CHUNK_SIZE, cz * CHUNK_SIZE)))

        if chunk_index == -1:
            return None
        
        chunk = self.world.chunks[chunk_index]
        if not chunk:
            self.world.build_chunk(cx, cy, cz)
        chunk = self.world.chunks[chunk_index]

        chunk.build_mesh()
    def rebuild_adj_chunks(self, chunk_position, local_voxel_pos):
        cx, cy, cz = chunk_position
        lx, ly, lz = local_voxel_pos

        chunk_positions = [
            (cx + 1, cy, cz), (cx - 1, cy, cz),
            (cx, cy + 1, cz), (cx, cy - 1, cz),
            (cx, cy, cz + 1), (cx, cy, cz - 1)
        ]

        for pos in chunk_positions:
            self.rebuild_chunk(*pos)

    def setblock(self, wx, wy, wz, voxel_id, data={}):

        chunk_index = (get_chunk_index((wx, wy, wz)))
        if not chunk_index in range(WORLD_VOL) or chunk_index == -1:
            return 0
        
        chunk = self.world.chunks[chunk_index]
        if not chunk:
            self.world.build_chunk(wx // CHUNK_SIZE, wy // CHUNK_SIZE, wz // CHUNK_SIZE)
        chunk = self.world.chunks[chunk_index]

        cx, cy, cz = chunk.position
        cx *= CHUNK_SIZE
        cy *= CHUNK_SIZE
        cz*= CHUNK_SIZE
        lx, ly, lz = wx - cx, wy - cy, wz - cz

        local_voxel_position = (get_index(lx, ly, lz))
        # chunk.light_map = self.world.chunk_light(chunk.voxels)

        self.world.voxels[chunk_index][local_voxel_position] = voxel_id
        if voxel_id == 0 and self.getblock(wx, wy + 1, wz) == TORCH:
            self.setblock(wx, wy + 1, wz, 0)
  

        chunk.voxels[local_voxel_position] = voxel_id
        chunk.build_mesh()



        self.rebuild_adj_chunks(chunk.position, (lx, ly, lz))

        return 1
    def ray_cast(self):

        # start point
        x1, y1, z1 = self.app.player.position + self.app.player.forward
        # end point
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            entity_targeted, entity = self.app.entity_handler.entity_at((current_voxel_pos.x, current_voxel_pos.y, current_voxel_pos.z))
            result = self.get_block(current_voxel_pos.x, current_voxel_pos.y, current_voxel_pos.z)
            if result[0] not in [0, WATER_FULL]:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos



                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True
            
            elif entity_targeted:
                self.voxel_id = None
                self.voxel_world_pos = None
                self.voxel_index = None
                self.voxel_local_pos = None
                self.voxel_normal = None
                self.entity = entity
                return True


            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2


        
        self.voxel_id = None
        self.voxel_world_pos = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_normal = None
        self.entity = None

        return False
    
    @staticmethod
    @njit
    def _grab(world_voxels, x1, x2, y1, y2, z1, z2):
        x_size = x2 - x1
        y_size = y2 - y1
        z_size = z2 - z1
        
        blocks = np.empty((x_size, y_size, z_size))
        for rx in range(x_size):
            for ry in range(y_size):
                for rz in range(z_size):
                    if rx < 0 or rx > WORLD_W * CHUNK_SIZE or ry < 0 or ry > WORLD_Y or rz < 0 or rz > WORLD_D * CHUNK_SIZE:
                        blocks[rx][ry][rz] = 0

                    x = rx + x1
                    y = ry + y1
                    z = rz + z1
                    chunk_voxels = world_voxels[get_chunk_index((x, y, z))]
                    cx = (x // CHUNK_SIZE) * CHUNK_SIZE
                    cy = (y // CHUNK_SIZE) * CHUNK_SIZE
                    cz = (z // CHUNK_SIZE) * CHUNK_SIZE
                    lx = cx - x
                    ly = cy - y
                    lz = cz - z
                    blocks[rx][ry][rz] = chunk_voxels[get_index(lx, ly, lz)]
        return blocks
    def grab(self, x1, x2, y1, y2, z1, z2):
        return self._grab(self.world.voxels, uint16(x1), uint16(x2), uint16(y1), uint16(y2), uint16(z1), uint16(z2))
   
  
