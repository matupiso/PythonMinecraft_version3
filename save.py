from settings import *
import os
from world_objects.item import InventoryItem



def save_world(world_name, world):
    if not os.path.exists(f"worlds\\{world_name}"):
        os.mkdir(f"worlds\\{world_name}")
    for chunk in world.chunks:
        if chunk:
            save_chunk(world_name, chunk)

    save_player(world_name, world.app.player)

    if os.path.exists(f"worlds\\{world_name}\\seed.www"):
        with open(f"worlds\\{world_name}\\seed.www", "w") as f:
            f.write(str(SEED))
    else:
        with open(f"worlds\\{world_name}\\seed.www", "x") as f:
            f.write(str(SEED))

    
def save_chunk(world_name,  chunk):
    x,y,z = chunk.position
    fname = f"cx{x}y{y}z{z}"
    if os.path.exists(f"worlds\\{world_name}\\{fname}.www"):
        with open(f"worlds\\{world_name}\\{fname}.www", "w") as f:
            f.write("/".join(list(map(lambda x: str(x), chunk.voxels))))
    else:
        with open(f"worlds\\{world_name}\\{fname}.www", "x") as f:
            f.write("/".join(list(map(lambda x: str(x), chunk.voxels))))

def chunk_is_generated(world_name, position):
    x,y,z = position
    if os.path.exists(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www"):
        with open(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www") as f:
            data = f.read()
        if "/" in data and data.replace("/", "").isdigit():
            return True
        
    return False
def world_exists(world_name):
    return os.path.exists(f"worlds\\{world_name}")

def save_player(world_name, player):
    player_data = f"{player.position.x}\n{player.position.y}\n{player.position.z}\n{".".join(list(map(lambda x: str(x), player.inventory.slots)))}\n{player.velocity}\n{player.yaw}\n{player.pitch}\n{GAMEMODE}"

    if os.path.exists(f"worlds\\{world_name}\\player.www"):
        with open(f"worlds\\{world_name}\\player.www", "w") as f:
            f.write(player_data)
    else:
        with open(f"worlds\\{world_name}\\player.www", "x") as f:
            f.write(player_data)

def load_chunk(world_name, position):
    x,y,z = position
    with open(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www", 'r') as f:
        data = list(map(lambda x: int(x), f.read().split("/")))

    if len(data) == CHUNK_VOL:
        return np.array(data, dtype="uint8")
    

    else:
        return np.append(np.array(data, dtype='uint8'), np.zeros(CHUNK_VOL - len(data), dtype='uint8'))
    

def load_player(world_name, player):
    with open(f"worlds\\{world_name}\\player.www", 'r') as f:
        data = f.read().split("\n")



    player.position = glm.vec3(float(data[0]),  
                               float(data[1]), 
                               float(data[2]))
    
    # player.inventory.slots = list(
    #     map(lambda x: 0 if x == "0" else InventoryItem(int(x.split("n")[0], int(x.split("n")[1]))), data[3].split("."))
    #     )
    
    player.velocity = float(
        data[4]
    )

    player.yaw = float(
        data[5]
    )

    player.pitch = float(
        data[6]
    )

    import settings as st
    st.GAMEMODE = int(data[7])
    del st

    


def get_seed(world_name):
    with open(f"worlds\\{world_name}\\seed.www", 'r') as f:
        return int(f.read())