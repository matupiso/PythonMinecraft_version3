from settings import *
from frustom import Frustum



class Camera:
    def __init__(self, position, yaw, pitch):

        self.last_pos_xz = glm.vec3(position)

        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)
        self.on = True


        self.deform = glm.vec3(0, 0, 0)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        self.frustom = Frustum(self)


    def update(self):
        self.update_vectors()
        self.update_view_matrix()

        
    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position + self.deform, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))
    def move_b(self, position):
        if not self.on: return
        can_x = self.app.collisions.player_can_move_forward_x(self.position) if position.x >= 0 else self.app.collisions.player_can_move_backward_x(self.position)
        can_z = self.app.collisions.player_can_move_forward_z(self.position) if position.z >= 0 else self.app.collisions.player_can_move_backward_z(self.position)


        self.position += glm.vec3(position.x, 0, 0) if can_x else glm.vec3(0, 0, 0)
        self.position += glm.vec3(0, 0, position.z) if can_z else glm.vec3(0, 0, 0)
        self.last_pos_xz = self.position

        if (not can_x and not can_z) or glm.ivec3(self.position) == glm.ivec3(self.last_pos_xz): return

        b = self.app.collisions.get_vid(self.position - glm.vec3(0, PLAYER_HEIGHT, 0))

        
        name = BLOCK_NAMES[BLOCKS.index(b)].lower()
        self.app.sound.playsound(f"minecraft.blocks.{name}.walk", volume=0.8)




        
    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        self.move_b(-(self.right * velocity * glm.vec3(1, 0, 1)))

    def move_right(self, velocity):
        self.move_b(self.right * velocity * glm.vec3(1, 0, 1))

    def move_up(self, velocity):
        self.position += self.up * velocity * glm.vec3(0, 1, 0)

    def move_down(self, velocity):
        self.position -= self.up * velocity * glm.vec3(0, 1, 0)

    def move_forward(self, velocity):
        self.move_b(self.forward * velocity * glm.vec3(1, 0, 1))

    def move_back(self, velocity):
        self.move_b(-(self.forward * velocity * glm.vec3(1, 0, 1)))









