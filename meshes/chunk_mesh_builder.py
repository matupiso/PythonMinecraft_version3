from settings import *
from numba import uint8, float32
from utils import can_bcm_block, is_transparent, water_is_transparent

#special tex types 
TORCH_SIDE = 1
TORCH_TOP = 0

TF_1 = 2
TF = 3
TF_3 = 4
TF_4 = 5
TF_5 = 6
TF_6 = 7
GLASS_SIDE = 8

@njit
def to_uint8(x, y, z, voxel_id, face_id, ao_id, light_id, crack_id):
    return uint8(x),uint8(y),uint8(z),uint8(voxel_id),uint8(face_id),uint8(ao_id),uint8(light_id),uint8(crack_id)


@njit
def to_float32(x, y, z, tex_type, ux, uy):
    return float32(x), float32(y), float32(z), float32(tex_type), float32(ux), float32(uy)

@njit
def get_chunk_index(world_pos):
    wx, wy, wz = world_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1
    
    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index

@njit
def get_ao(voxels_pos, world_pos, world_voxels, plane):
    x, y, z = voxels_pos
    wx, wy, wz = world_pos
    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)
        c = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        d = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        g = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        h = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
    elif plane == "X":
        a = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        b = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)
        c = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        d = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        e = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        f = is_void((x ,y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        g = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        h = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)

    else: #Z plane
        a = is_void((x, y + 1, z), (wx, wy + 1, wz),  world_voxels)
        b = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        c = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, z), world_voxels)
        e = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        f = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        g = is_void((x - 1, y, z), (wx - 1, y, z), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    return [a + b + c, c + d + e, e + f + g, g + h + a]

@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y

@njit
def is_void(voxel_pos, world_pos, world_voxels, water=False):
    chunk_index = int(get_chunk_index(world_pos))
    if chunk_index == -1:
        return True
    
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    if ((is_transparent(chunk_voxels[voxel_index])) and not water) or (water and water_is_transparent(chunk_voxels[voxel_index])):
        return True
    return False

@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for vertecie in vertex:
            vertex_data[index] = vertecie
            index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_position, world_voxels, light_map, crack_pos, crack_index, transparent_mesh = False):
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')
    index = 0
    rx,ry,rz = crack_pos if crack_pos else (0, 0, 0)

    rx = int(rx)
    ry = int(ry)
    rz = int(rz)

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[get_index(x, y, z)]
                light_id = light_map[get_index(x, y, z)]
         
               
                if not voxel_id or not can_bcm_block(voxel_id) or (is_transparent(voxel_id) and transparent_mesh == False) or (not is_transparent(voxel_id)  and transparent_mesh == True): continue
                #voxel world pos
                cx, cy, cz = chunk_position
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                is_cracked = (rx == wx and ry == wy and rz == wz)


                is_water = voxel_id == WATER_FULL
                
                
                
                
             



                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels, water=is_water):
                    # format: x, y, z, voxel_id, face_id, ao_id

                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, "Y")
                    v0 = to_uint8(x    , y + 1, z    , voxel_id, 0, ao[3], light_id, crack_index if is_cracked else 6)
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 0, ao[0], light_id, crack_index if is_cracked else 6)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[1], light_id, crack_index if is_cracked else 6)
                    v3 = to_uint8(x    , y + 1, z + 1, voxel_id, 0, ao[2], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels, water=is_water):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, "Y")

                    v0 = to_uint8(x    , y, z    , voxel_id, 1, ao[3], light_id, crack_index if is_cracked else 6)
                    v1 = to_uint8(x + 1, y, z    , voxel_id, 1, ao[0], light_id, crack_index if is_cracked else 6)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1, ao[1], light_id, crack_index if is_cracked else 6)
                    v3 = to_uint8(x    , y, z + 1, voxel_id, 1, ao[2], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels, water=is_water):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, "X")                    

                    v0 = to_uint8(x + 1, y    , z    , voxel_id, 2, ao[2], light_id, crack_index if is_cracked else 6)
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 2, ao[3], light_id, crack_index if is_cracked else 6)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[0], light_id, crack_index if is_cracked else 6)
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 2, ao[1], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels, water=is_water):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, "X")     

                    v0 =  to_uint8(x, y    , z    , voxel_id, 3, ao[2], light_id, crack_index if is_cracked else 6)
                    v1 =  to_uint8(x, y + 1, z    , voxel_id, 3, ao[3], light_id, crack_index if is_cracked else 6)
                    v2 =  to_uint8(x, y + 1, z + 1, voxel_id, 3, ao[0], light_id, crack_index if is_cracked else 6)
                    v3 =  to_uint8(x, y    , z + 1, voxel_id, 3, ao[1], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels, water=is_water):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, "Z")

                    v0 = to_uint8(x,     y,     z, voxel_id, 4, ao[2], light_id, crack_index if is_cracked else 6)
                    v1 = to_uint8(x,     y + 1, z, voxel_id, 4, ao[3], light_id, crack_index if is_cracked else 6)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4, ao[0], light_id, crack_index if is_cracked else 6)
                    v3 = to_uint8(x + 1, y,     z, voxel_id, 4, ao[1], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels, water=is_water):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, "Z")

                    v0 = to_uint8(x    , y    , z + 1, voxel_id, 5, ao[2], light_id, crack_index if is_cracked else 6)
                    v1 = to_uint8(x    , y + 1, z + 1, voxel_id, 5, ao[3], light_id, crack_index if is_cracked else 6)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[0], light_id, crack_index if is_cracked else 6)
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 5, ao[1], light_id, crack_index if is_cracked else 6)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]

@njit
def build_chunk_mesh_special(chunk_voxels, format_size, torch_index):
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='float32')
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id or  can_bcm_block(voxel_id): continue   



                if voxel_id == TORCH:
                    flame = TF_1 + torch_index
                    #flame
                    v0 = to_float32(x + 0.4,y + 0.855,     z + 0.4, flame, 0, 1)
                    v1 = to_float32(x + 0.4,y + 1.0, z + 0.4, flame, 0, 0)
                    v2 = to_float32(x + 0.55, y + 1.0, z + 0.55, flame, 1, 0)
                    v3 = to_float32(x + 0.55, y + 0.855,     z + 0.55, flame, 1, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                    v0 = to_float32(x + 0.4,y + 0.855,     z + 0.55, flame, 0, 1)
                    v1 = to_float32(x + 0.4,y + 1.0, z + 0.55, flame, 0, 0)
                    v2 = to_float32(x + 0.55, y + 1.0, z + 0.4, flame, 1, 0)
                    v3 = to_float32(x + 0.55, y + 0.855,     z + 0.4, flame, 1, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)


                    #top
                    v0 = to_float32(x + 0.4 , y + 0.8, z + 0.4   , TORCH_TOP, 0, 0)
                    v1 = to_float32(x + 0.55, y + 0.8, z + 0.4  , TORCH_TOP, 1, 0)
                    v2 = to_float32(x + 0.55, y + 0.8, z + 0.55, TORCH_TOP, 1, 1)
                    v3 = to_float32(x + 0.4, y + 0.8, z + 0.55, TORCH_TOP, 0, 1)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # right
              
                    v0 = to_float32(x + 0.55, y    , z  + 0.4 , TORCH_SIDE, 1, 1)
                    v1 = to_float32(x + 0.55, y + 0.8, z  + 0.4, TORCH_SIDE, 1, 0)
                    v2 = to_float32(x + 0.55, y + 0.8, z + 0.55, TORCH_SIDE, 0, 0)
                    v3 = to_float32(x + 0.55, y    , z + 0.55, TORCH_SIDE, 0, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left
             
                    v0 =  to_float32(x + 0.4, y    , z + 0.4, TORCH_SIDE, 1, 1)
                    v1 =  to_float32(x + 0.4, y + 0.8, z + 0.4, TORCH_SIDE, 1, 0)
                    v2 =  to_float32(x + 0.4, y + 0.8, z + 0.55, TORCH_SIDE, 0, 0)
                    v3 =  to_float32(x + 0.4, y    , z + 0.55, TORCH_SIDE, 0, 1)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back 
            
                    v0 = to_float32(x + 0.4,y,     z + 0.4, TORCH_SIDE, 0, 1)
                    v1 = to_float32(x + 0.4,y + 0.8, z + 0.4, TORCH_SIDE, 0, 0)
                    v2 = to_float32(x + 0.55, y + 0.8, z + 0.4, TORCH_SIDE, 1, 0)
                    v3 = to_float32(x + 0.55, y,     z + 0.4, TORCH_SIDE, 1, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front
                    v0 = to_float32(x + 0.4, y    , z + 0.55, TORCH_SIDE, 0, 1)
                    v1 = to_float32(x + 0.4, y + 0.8, z + 0.55, TORCH_SIDE, 0, 0)
                    v2 = to_float32(x + 0.55, y + 0.8, z + 0.55, TORCH_SIDE, 1, 0)
                    v3 = to_float32(x + 0.55, y    , z + 0.55, TORCH_SIDE, 1, 1)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                elif voxel_id == GLASS:



                   
                    v0 = to_float32(x    , y + 1, z    , GLASS_SIDE,    0, 0)
                    v1 = to_float32(x + 1, y + 1, z    , GLASS_SIDE,    1, 0)
                    v2 = to_float32(x + 1, y + 1, z + 1, GLASS_SIDE,    1, 1)
                    v3 = to_float32(x    , y + 1, z + 1, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

            
              
                   

                    v0 = to_float32(x    , y, z    , GLASS_SIDE,    0, 0)
                    v1 = to_float32(x + 1, y, z    , GLASS_SIDE,    1, 0)
                    v2 = to_float32(x + 1, y, z + 1, GLASS_SIDE,    1, 1)
                    v3 = to_float32(x    , y, z + 1, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                
                           

                    v0 = to_float32(x + 1, y    , z    , GLASS_SIDE,    1, 1)
                    v1 = to_float32(x + 1, y + 1, z    , GLASS_SIDE,    1, 0)
                    v2 = to_float32(x + 1, y + 1, z + 1, GLASS_SIDE,    0, 0)
                    v3 = to_float32(x + 1, y    , z + 1, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

               
         
                    

                    v0 =  to_float32(x, y    , z    , GLASS_SIDE,    1, 1)
                    v1 =  to_float32(x, y + 1, z    , GLASS_SIDE,    1, 0)
                    v2 =  to_float32(x, y + 1, z + 1, GLASS_SIDE,    0, 0)
                    v3 =  to_float32(x, y    , z + 1, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

              
            
                   

                    v0 = to_float32(x,     y,     z, GLASS_SIDE,    1, 1)
                    v1 = to_float32(x,     y + 1, z, GLASS_SIDE,    1, 0)
                    v2 = to_float32(x + 1, y + 1, z, GLASS_SIDE,    0, 0)
                    v3 = to_float32(x + 1, y,     z, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)


                  

                    v0 = to_float32(x    , y    , z + 1, GLASS_SIDE,    1, 1)
                    v1 = to_float32(x    , y + 1, z + 1, GLASS_SIDE,    1, 0)
                    v2 = to_float32(x + 1, y + 1, z + 1, GLASS_SIDE,    0, 0)
                    v3 = to_float32(x + 1, y    , z + 1, GLASS_SIDE,    0, 1)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)


    return vertex_data[:index + 1]





