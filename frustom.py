from settings import *
from utils import get_distance, calc_yaw_pitch
from meshes.chunk_mesh_builder import get_chunk_index

class Frustum:
    def __init__(self, camera):
        self.cam = camera

        self.factor_y = 1.0 / math.cos(half_y := V_FOV * 0.5)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV * 0.5)
        self.tan_x = math.tan(half_x)

        print_info("state: frustum_initialized")

    def is_on_frustum(self, chunk):
         
        # vector to sphere center
        sphere_vec = chunk.center - self.cam.position

        # outside the NEAR and FAR planes?
        sz = glm.dot(sphere_vec, self.cam.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= (FAR - 4) + CHUNK_SPHERE_RADIUS):
            return False

        # outside the TOP and BOTTOM planes?
        sy = glm.dot(sphere_vec, self.cam.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        # outside the LEFT and RIGHT planes?
        sx = glm.dot(sphere_vec, self.cam.right)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        return True
    

    def is_visible(self, chunk):
        wx, wy, wz = glm.vec3(*chunk.position) * CHUNK_SIZE
        cx, cy, cz = glm.vec3(*chunk.position)

        cam_position = glm.vec3(self.cam.position) // CHUNK_SIZE

        if get_distance((wx, wy, wz), glm.vec3(self.cam.position)) > FAR:
            return False
        
        camera_r = 1
        baricadings = False

        while True:
            pitch, yaw = calc_yaw_pitch(cam_position, chunk.position)
            forward = glm.vec3(0, 0, 0)

            forward.x = glm.cos(yaw) * glm.cos(pitch)
            forward.y = glm.sin(pitch)
            forward.z = glm.sin(yaw) * glm.cos(pitch)

            position = cam_position + (forward * camera_r)

            chunk_index = get_chunk_index(position.x, position.y, position.z)
            if chunk_index == -1:
                break



            world = chunk.world
            targeted_chunk = world.chunks[chunk_index]

            if targeted_chunk is chunk: break

            
            if targeted_chunk.is_full:
                baricadings = True

            

        return not baricadings
            


def chunk_in_reach(player_pos, cx, cz):
    px, py, pz = player_pos

    px //= CHUNK_SIZE
    pz //= CHUNK_SIZE

    if glm.abs(px - cx) <= PLAYER_CHUNK_FAR and glm.abs(pz - cz) <= PLAYER_CHUNK_FAR:
        return True
    
    return False