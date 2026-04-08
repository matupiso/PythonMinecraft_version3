from settings import *
from noise import noise2, noise3, octaveNoise
from meshes.chunk_mesh_builder import get_index
@njit
def abs_float(x:float):
    if x >= 0.0: return x
    elif x < 0.0: return float(-x)
    return 0.0


# @njit
# def get_height(x, z):
#     # island mask
#     # island = 1 / (pow(0.0025 * math.hypot(x - CENTER_X, z - CENTER_Z), 20) + 0.0001)
#     # island = min(island, 1)

#     # amplitude
#     a1 = CENTER_Y
#     a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125
 

#     # frequency
#     f1 =  abs_float(0.03 * noise2(x * 0.001, z * 0.001)) * 0.0003
#     f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

#     # if noise2(0.1 * x, 0.1 * z) < 0:
#     #     a1 /= 1.0001

#     height = 0
#     height += noise2(x * f1, z * f1) * a1 + a1
#     height += noise2(x * f2, z * f2) * a2 - a2
#     height += noise2(x * f4, z * f4) * a4 + a4
#     height += noise2(x * f8, z * f8) * a8 - a8

#     height = max(height,  noise2(x * f8, z * f8) + 2)


#     return int(height) + 32
@njit
def get_height(x, z):
    f1,f2,f3,f4 = 0.004, 0.04, 0.1, 0.01
    a1, a2, a3, a4 = 0.004, 0.02, 0.00001, 0.06
    noise = 0
    noise += noise2(x * f1, z * f1) * a1
    noise += noise2(x * f2, z * f2) * a2
    noise += noise2(x * f3, z * f3) * a3
    noise += noise2(x * f4, z * f4) * a4



    
    noise /= (a1 + a2 + a3 + a4)

    if noise2(x * f1, z * f1) * a1 < 0:
        noise += 0.02 + -noise2(x * f1,  z * f1) * 0.045
    height = int(noise * 80) + 100


    return height 

# @njit
# def get_height(x, z):
#     h1 = ((noise2(x * 0.0005, z * 0.0005) + 1) / 2) * 0.0099
#     h2 = noise2(x * h1, z * h1)
#     height = h2 * CHUNK_SIZE
#     return int(height) + 2 * CHUNK_SIZE

# @njit
# def _get_height(x, z):

#     h1 = noise2(x * 0.09, z * 0.09)
#     h2 = noise2(x * 0.18, z * 0.18)
#     h3 = noise2(x * 0.0902, z * 0.0902)
#     h4 = noise2(x * 0.04, z * 0.04)

#     height = 0
#     if h2 < h1: height = h2
#     elif h1 < h2: height = h1
#     else:
#         height = 2 * h1
#     return int(height * 32)  + (int(90 * (h3 - 0.3) if h3 > 0.46 else 0) if h4 > 0.44 and h4 < 0.6 else 0) + 56

# @njit
# def get_height(x, z):
#     n1 = noise2(x * 0.024, z * 0.024) 
#     if n1 <= 0:n1 = 0.1
#     n2 = noise2(x * n1, z * n1)
#     return int(n2 * 22) + 32
#     # h_select = noise2(x * 0.002, z * 0.002)
#     # if h_select > 0.59:
#     #     return _get_height(x, z)
#     # else:
#     #     return int((h_select - 0.31) * 32) + 32





@njit
def get_temperature(x, z):
    raw_temp = noise2(x * 0.001, z * 0.001)


    indicator = 1 if raw_temp > 0.005 else -1
    if raw_temp  == 0.005: indicator = 0
    raw_temp = abs_float(raw_temp)
    raw_temp *= 100
    raw_temp = int(raw_temp)
    


    temp = raw_temp + (indicator if x % (z // 10 + 1) > 10 else -1)

    return temp

@njit
def get_humdity(x, z):
    wh = get_height(x, z)
    raw_hum = noise2(x * 0.002, z * 0.0002)
    raw_hum = int(raw_hum * 100)
    if wh > 100: ind = 0.005
    else: ind  = 0.0001

    ind *= int(noise2(x, z) * 100)
    ind += random.randrange(0, 10) / 10

    hum = raw_hum + ind
    hum = abs_float(hum)
    return hum

def get_biome(x, z):
    world_height = get_height(x, z)
    temperature = get_temperature(x, z)
    humdity = get_humdity(x, z, world_height)
    biome = 0

    if world_height > MOUNTIN_MIN_HEIGHT:
        if temperature > 20:
            biome = MOUNTIN_HOT

        else:
            biome = MOUNTIN_COLD


    elif world_height <= MOUNTIN_LVL and world_height > PLAIN_MIN_HEIGHT:
        if temperature > 40:
            biome = DESERT

        else:
            biome = PLAINS

    elif world_height <= PLAIN_MIN_HEIGHT and world_height > SEA_MIN_HEIGHT:
        biome = 0


    return biome


@njit
def noise_int(x, z, f, a, b):
    n = noise2(x * f, z * f)
    n += 1
    n /= 2
    r = (n * (b - a)) + a
    if r > b: r= b
    if r < a: r = a
    return r


@njit
def coal_ore_vein(x, y, z):
    la = (COAL_ORE_LEVEL_A - (WORLD_Y - get_height(x, z)))
    lb = (COAL_ORE_LEVEL_B - (WORLD_Y - get_height(x, z)))
    

    p = noise3(x * 0.201, y * 0.201, z * 0.201)
    if y < lb and y > la:
        p *= 1.05
    elif y < la:
        p *= 1.001
    elif y > lb:
        p *= 0.84

    return p > 0.5
        


@njit
def diamond_ore_vein(x, y, z):
    la = (DIAMOND_ORE_LEVEL_A - (WORLD_Y - get_height(x, z)))
    lb = (DIAMOND_ORE_LEVEL_B - (WORLD_Y - get_height(x, z)))
    

    if y > la + 6:
        return False
    f = 0.2
    if y > la:
        f *= 1 / (y - la)
    elif y < lb:
        f *= 1 / (lb - y)
    p = noise3(x * f, y * f, z * f)
    return p < -0.7
   


@njit
def get_VH_height(x, z, plus, minus):

    

    freq = 1.56

    height = noise2(x * freq, z * freq)
    height *= freq + 1
    height = int(height * 4.19)
    height = min(plus, height)
    height = max(minus, height)
    return height

@njit
def set_voxel_id_plains(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = GRASS


@njit
def set_voxel_id_desert(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = SAND


@njit
def set_voxel_id_mountin_hot(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = STONE


@njit
def set_voxel_id_mountin_cold(voxels, x, y, z, wx, wy, wz):
    voxels[get_index(x, y, z)] = SNOW

@njit
def math_abs(x):
    return x if x > 0 else -x


@njit
def is_cave(x, y, z):
    n1 = noise3(x * 0.01, y * 0.01, z * 0.01)
    n2 = noise3(x * 0.07, y * 0.07, z * 0.07)
    n3 = noise3(x * 0.0001, y * 0.0001, z * 0.0001)


    if (abs_float(n1) < 0.0999 and abs_float(n2) < 0.0999) ^ (n3 > 0.02 and y < get_height(x, z) - 30):

        return True
    return False

@njit
def is_river(x, y, z):
    n1 = abs_float(noise2(x * 0.08, z * 0.08))
    n2 = abs_float(noise2(x * 0.02, z * 0.02))

    if n1 < 0.09 and n2 < 0.09 and y > (n1 * n2 * 50):
            return True
        
    return False
@njit
def is_riversand(x, y, z):
    n1 = abs_float(noise2(x * 0.08, z * 0.08))
    n2 = abs_float(noise2(x * 0.02, z * 0.02))

    if n1 > 0.09 and n1 < 0.1 and n2 > 0.09 and n2 < 0.1:
        if y < get_height(x, z) - (n1 * n2 * 40) + 10 and y > get_height(x, z) - (n1 * n2 * 40) - 10:
            return True
        
    return False

@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz):

    world_height = get_height(wx, wz)
    if wy == 0:
        voxel_id = BEDROCK
    elif wy >= MOUNTIN_LVL + get_VH_height(wx, wz, MOUNTIN_PLUS, MOUNTIN_MINUS) and wy < SNOW_LVL + get_VH_height(wx, wz, SNOW_PLUS, SNOW_MINUS):
        voxel_id = STONE if random.random() > 0.1 else COAL_ORE



    elif wy == world_height - 1:
        voxel_id = SAND if (get_temperature(wx, wz) > 64) else GRASS 
    elif wy < world_height - 1 and wy > noise_int(x, z, 0.95, world_height - 10, world_height - 4):
        voxel_id = SAND if (get_temperature(wx, wz) > 64) else DIRT 

    if is_cave(wx, wy, wz):
        if voxel_id != BEDROCK:
            voxels[get_index(x, y, z)] = 0
            return

        # if  wy < world_height - 2 and y > 1 and wy < MOUNTIN_LVL and noise_int(x, z, 0.34, 0, 90) == 3:
        #     voxels[get_index(x, y-1, z)] = WOOD 
        #     voxel_id = TORCH

    else:
        if coal_ore_vein(wx, wy, wz) and not voxel_id in [GRASS, DIRT, BEDROCK]:
            voxel_id = COAL_ORE
    
        elif diamond_ore_vein(wx, wy, wz) and not voxel_id in [GRASS, DIRT, BEDROCK]:
            voxel_id = DIAMOND_ORE

        else:
            if not voxel_id in [GRASS, DIRT, BEDROCK]:
                voxel_id = STONE





    if voxel_id == GRASS and wy >= MOUNTIN_LVL + get_VH_height(wx, wz, MOUNTIN_PLUS, MOUNTIN_MINUS):
        voxel_id = STONE
    elif voxel_id == DIRT and is_riversand(x, y, z):
        voxel_id = SAND


    if voxel_id == GRASS:
        if noise_int(x, z, 0.99, 0,  100) < 10:
            place_tree(voxels, x, y, z, wy)
    if is_river(wx, wy, wz) or wy > world_height:
        voxel_id = WATER_FULL
    if voxel_id == DIRT and is_riversand(x, y, z):
            voxel_id = SAND

    

    voxels[get_index(x, y, z)] = voxel_id


@njit
def place_tree(voxels, x, y, z,  wy):
    TREE_HEIGHT = random.randint(TREE_MIN_HEIGHT, TREE_MAX_HEIGHT)
    TREE_H_HEIGHT = TREE_HEIGHT // 2  
    TREE_H_WIDTH = random.randint(TREE_MIN_WIDTH, TREE_MAX_WIDTH) // 2

    rnd = random.random()
        
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if wy > MOUNTIN_LVL - MOUNTIN_VARIABILITY - 1:
        return None





    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random.random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES



@njit
def place_bush(voxels, x, y, z,  wy):
    TREE_HEIGHT = BUSH_HEIGHT
    TREE_H_HEIGHT = TREE_HEIGHT // 2  
    TREE_H_WIDTH = random.randint(TREE_MIN_WIDTH, TREE_MAX_WIDTH) // 2

    rnd = random.random()
        
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if wy > MOUNTIN_LVL - MOUNTIN_VARIABILITY - 1:
        return None

    # wood under the tree





    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random.random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES


