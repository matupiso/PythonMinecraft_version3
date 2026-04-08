import glm
from settings import *
class Collider:
    def __init__(self, pos1, pos2):
        self.x1 = pos1.x
        self.y1 = pos1.y
        self.z1 = pos1.z

        self.x2 = pos2.x
        self.y2 = pos2.y
        self.z2 = pos2.z

        self.pos1 = pos1
        self.pos2 = pos2

        
        


    def __add__(self, pos):
        return Collider(pos + self.pos1, pos + self.pos2)
    

    def __and__(self, collider):
        x = min(self.pos2.x, collider.pos2.x) - max(self.pos1.x, collider.pos1.x)
        y = min(self.pos2.y, collider.pos2.y) - max(self.pos1.y, collider.pos1.y)
        z = min(self.pos2.z, collider.pos2.z) - max(self.pos1.z, collider.pos1.z)

        return x > 0 and y > 0 and z > 0
    
    def collide(self, collider, velocity):
        vx, vy, vz = velocity

        time = lambda x, y: x / y if y else float("-" * (x > 0) + "inf")

        x_entry = time(collider.x1 - self.x2 if vx > 0 else collider.x2 - self.x1,vx)
        x_exit =  time(collider.x2 - self.x1 if vx > 0 else collider.x1 - self.x2,vx)

        y_entry = time(collider.y1 - self.y2 if vy > 0 else collider.y2 - self.y1,vy)
        y_exit =  time(collider.y2 - self.y1 if vy > 0 else collider.y1 - self.y2,vy)

        z_entry = time(collider.z1 - self.z2 if vz > 0 else collider.z2 - self.z1,vz)
        z_exit =  time(collider.z2 - self.z1 if vz > 0 else collider.z1 - self.z2,vz)

        if x_entry < 0 and y_entry < 0 and z_entry < 0:
            return 1, None
        if x_entry > 1 and y_entry > 1 and z_entry > 1:
            return 1, None
        
        entry = max(x_entry, y_entry, z_entry)
        exit_ = min(x_exit, y_exit, z_exit)

        if entry > exit_:
            return 1, None
        
        nx = (0, -1 if vx > 0 else 1)[entry==x_entry]
        ny = (0, -1 if vy > 0 else 1)[entry==y_entry]
        nz = (0, -1 if vz > 0 else 1)[entry==z_entry]
        return entry, (nx, ny, nz)
        
        

        
player_collider = (
    glm.vec3(0, 0, 0), glm.vec3(1, PLAYER_HEIGHT, 1)
)

cube_block_collider = (
    glm.vec3(0, 0, 0), glm.vec3(1, 1, 1)
)

torch_block_collider = (
    glm.vec3(0.385, 0, 0.385), glm.vec3(0.615, 0.9, 0.615)
)

def get_block_collider(block:int):
    return torch_block_collider if block == TORCH else cube_block_collider