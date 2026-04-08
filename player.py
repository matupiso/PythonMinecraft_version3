from settings import *
from camera import Camera
import pygame as pg
from utils import is_breakable, is_climbable, to_surival_mined, get_dig_time,  get_damage
from world_objects.entity import player_entity
from world_objects.item import InventoryItem as Item
from time import time
from textures import replace_color, water_on_screen
from terrian_gen import get_height
from inventory import *




class Player(Camera):
    def __init__(self, app, position=PLAYER_START_POS, yaw=-90, pitch=0, gravity=0.1, velocity_at_jump=0.5, velocity_at_fall=-0.2):
        #initialize Camera and create an instance of main application
        
        self.app = app
        self.water_live_seconds = 0
        self.last_rbutton_state = False
        self.last_lbutton_state = False
        self.hand_angle_rel = 0  #70
        
        self.vaj = velocity_at_jump
        self.vaf = velocity_at_fall
        self.gravity = gravity
        self.velocity = 0 
        self.last_vel = 0
        self.not_jumping = True
        self.type = "player"
        self.name = "Steve"
        self.health = PLAYER_DEFAULT_HEALTH
        self.effects = {}
        self.seconds_timer = 0
        self.seconds_counter = 0


        self.full_heart_normal = pg.image.load("assets\\full_heart_normal.png")
        self.half_heart_normal = pg.image.load("assets\\half_heart_normal.png")

        self.full_heart_normal = pg.transform.scale(self.full_heart_normal, (60,60))
        self.half_heart_normal = pg.transform.scale(self.half_heart_normal, (60,60))

        self.full_heart_poison = pg.image.load("assets\\full_heart_poison.png")
        self.half_heart_poison = pg.image.load("assets\\half_heart_poison.png")

        self.full_heart_poison = pg.transform.scale(self.full_heart_poison, (60,60))
        self.half_heart_poison = pg.transform.scale(self.half_heart_poison, (60,60))

        self.full_heart_wither = pg.image.load("assets\\full_heart_wither.png")
        self.half_heart_wither = pg.image.load("assets\\half_heart_wither.png")

        self.full_heart_wither = pg.transform.scale(self.full_heart_wither, (60,60))
        self.half_heart_wither = pg.transform.scale(self.half_heart_wither, (60,60))

        self.empty_heart = pg.image.load("assets\\heart_empty.png")
        self.empty_heart = pg.transform.scale(self.empty_heart, (60,60))

        self.hotbar = pg.image.load("assets\\hot_bar.png")
        self.hotbar = pg.transform.scale(self.hotbar, (490,70))

        self.bubbele = pg.image.load("assets\\bubbele_icon.png")
        self.bubbele = pg.transform.scale(self.bubbele, (40,40))



        

        self.death_screen = pg.image.load("assets\\death_screen.png")
        self.death_screen_choice_r = pg.image.load("assets\\death_screen_choice_respawn.png")
        self.death_screen_choice_q = pg.image.load("assets\\death_screen_choice_quit.png")
        






        self.full_heart_normal = replace_color(self.full_heart_normal, (0, 0, 0), (1, 1, 1))
        self.half_heart_normal = replace_color(self.half_heart_normal, (0, 0, 0), (1, 1, 1))
        self.full_heart_poison = replace_color(self.full_heart_poison, (0, 0, 0), (1, 1, 1))
        self.half_heart_poison = replace_color(self.half_heart_poison, (0, 0, 0), (1, 1, 1))
        self.full_heart_wither = replace_color(self.full_heart_wither, (0, 0, 0), (1, 1, 1))
        self.half_heart_wither = replace_color(self.half_heart_wither, (0, 0, 0), (1, 1, 1))
        self.empty_heart = replace_color(self.empty_heart, (0, 0, 0), (1, 1, 1))

        self.can_float = False
        

        #inventory
        self.inventory = Inventory(app)


        self.held_item = 0
            
        self.hand_index = 0
        self._inventory_toggled = False
        self.bubbeles = 10
    
        self.dead = False
        self.hardcore_death = False
        self.spawn_point = PLAYER_START_POS

        self.can_fly = False
        self.in_water = False
    

        super().__init__(position, yaw, pitch)

       

        print_info("state: player_initialized")

    def can_ud(self):
        can_climb = False
        b1 = self.app.collisions.get_vid(self.position + glm.vec3(1, 0, 0))
        b2 = self.app.collisions.get_vid(self.position + glm.vec3(-1, 0, 0))
        b3 = self.app.collisions.get_vid(self.position + glm.vec3(0, 0, 1))
        b4 = self.app.collisions.get_vid(self.position + glm.vec3(0, 0, -1))

        b = [b1, b2, b3, b4]

        for i in b:
            if is_climbable(i):
                can_climb = True
                break


        can_swim = False

        return can_climb or can_swim
        


    def update(self):
        if self.on:
            
            super().update()
        self.mouse_controll()
        self.update_inventory()
        if not self.can_fly: self.handle_gravity()
        self.keyboard_controll()
        if self.dead:
            return
        if self.hand_angle_rel > 0:
            self.hand_angle_rel -= 1

        




        


        if time() - self.seconds_timer > 1:
            print(self.water_live_seconds)
            if self.in_water:
                self.water_live_seconds += 1

            else:
                self.water_live_seconds = 0
           
            if self.effects.get("poison") and self.health > 1:
                self.damage(1)
            if self.effects.get("wither"):
                self.damage(2,damage_content=["wither", ])
            if self.effects.get("regeneration") and self.health < 20:
                self.health += 1
            
            
            self.seconds_counter += 1
            if self.seconds_counter == 200:
                self.seconds_counter = 0
                
                
            if self.seconds_counter % 5 == 0:
                if self.bubbeles == 0:
                    self.damage(4, damage_content=['drown', ])

        
                
            if self.seconds_counter % 25 > 0 and self.in_water:
                if self.bubbeles > 0: self.bubbeles -= 1

            elif self.seconds_counter % 20 > 0 and not self.in_water:
                if self.bubbeles < 10: self.bubbeles += 1
            for key, item in self.effects.copy().items():
                self.effects[key] = item - 1
                if self.effects[key] <= 0:
                    del self.effects[key]

            

            self.seconds_timer = time()


    def render(self):
        self.can_float = False
        if self.app.voxel_handler.getblock(int(self.position.x), int(self.position.y), int(self.position.z)) == WATER_FULL:
                    self.app.scene.render_on_screen(water_on_screen, 0, 0)

                    self.in_water = True
                    self.can_float = True
        else:
            self.in_water = False
           


        if self.app.voxel_handler.getblock(int(self.position.x), int(self.position.y - 1), int(self.position.z)) == WATER_FULL:
            self.can_float = True


        

        self.app.scene.render_on_screen(self.hotbar, (WIN_RES.x - 423) // 2, int(WIN_RES.y * 0.80034) + 41)
        self.inventory.render_hotbar()





        if GAMEMODE == SURIVAL:

            if self.dead:
                x,y = pg.mouse.get_pos()
                if x > 392 and x < 759 and y > 200 and y < 279:
                    death_screen = self.death_screen_choice_r

                elif x > 392 and x < 759 and y > 310 and y < 389:
                    death_screen = self.death_screen_choice_q

                else:
                    death_screen = self.death_screen

                

                
                self.app.scene.render_on_screen(death_screen, 0, 0)
                self.app.scene.on_screen_tfi = 1




                return

            if "poison" in self.effects.keys():
                full_heart = self.full_heart_poison
                half_heart = self.half_heart_poison

            elif "wither" in self.effects.keys():
                full_heart = self.full_heart_wither
                half_heart = self.half_heart_wither

            else:
                full_heart = self.full_heart_normal
                half_heart = self.half_heart_normal

            

            if self.health % 2 == 0:
                h = [full_heart for i in range(self.health // 2)]
                for i in range(10 - self.health // 2):
                    h.append(self.empty_heart)
            else:
                h = [full_heart for i in range(self.health // 2)]
                h.append(half_heart)
                for i in range(9 - self.health // 2):
                    h.append(self.empty_heart)

            for i in range(10):
                self.app.scene.render_on_screen(h[i], i * 47 + (WIN_RES.x - 423) // 2, int(WIN_RES.y * 0.80034) - 19)

            if self.bubbeles != 10:
                for i in range(self.bubbeles):
                    self.app.scene.render_on_screen(self.bubbele, i * 47 + (WIN_RES.x - 423) // 2, int(WIN_RES.y * 0.80034) - 45)


        self.inventory.render()





     
        




    def inventory_on(self):
        if self.dead:
            return
        self.inventory.enabled = True
        self.on = False
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def inventory_off(self):
        if self.dead:
            return
        self.inventory.enabled = False
        self.on = True
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
    
        
    def update_inventory(self):
        self.held_item = self.inventory.get_hand_group()[self.hand_index]
        
        self.inventory.update()
    def respawn(self):
        
        self.on = True
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.position = glm.vec3(self.spawn_point)
        self.position.y = get_height(self.position.x,self.position.z) + 2

        self.dead = False
        self.effects = {}
        self.health = PLAYER_DEFAULT_HEALTH


   
    def mouse_controll(self):
        if self.dead:
                
            l, m, r = pg.mouse.get_pressed()
            x, y = pg.mouse.get_pos()

            if x > 392 and x < 759 and y > 200 and y < 279 and l:
                if self.hardcore_death:
                    self.app.is_running = False

                else: self.respawn()
            

            elif x > 392 and x < 759 and y > 310 and y < 389 and l:
                self.app.is_running = False
            



            return
        
        if not self.on:
            return
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        l, m, r = pg.mouse.get_pressed()




        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITVITY)

        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITVITY)
        voxel_handler = self.app.voxel_handler

        voxel_id = 0

        
        if not voxel_handler.voxel_id and not voxel_handler.entity:
            return 
        
        if voxel_handler.entity and self.last_rbutton_state == False and r == True:
            damage = get_damage(self.held_item.item_id if self.held_item else 0)
            damage_multiplyer = 1

            if self.velocity:
                damage_multiplyer += 0.9

            damage *= damage_multiplyer
            voxel_handler.entity.damage(damage)
    

        elif ((r == False and self.last_rbutton_state == True) or not voxel_handler.voxel_world_pos) and voxel_handler.world.crack_pos:
                crack_pos = glm.ivec3(voxel_handler.world.crack_pos)
                voxel_handler.world.crack_pos = None
                voxel_handler.world.acrack_index = None
                voxel_handler.rebuild_chunk(*(crack_pos // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)))
                voxel_handler.rebuild_adj_chunks((crack_pos // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)), crack_pos)
                
        elif voxel_handler.voxel_id and r and self.hand_angle_rel == 0:
            block_name = BLOCK_NAMES[BLOCKS.index(voxel_handler.voxel_id)].lower()
 
            if GAMEMODE == CREATIVE:
                self.app.sound.playsound(f"minecraft.blocks.{block_name}.destroy")
              
                voxel_handler.setblock(*glm.ivec3(voxel_handler.voxel_world_pos), 0)
            elif GAMEMODE == SURIVAL:
              
                if voxel_handler.world.crack_pos != glm.ivec3(voxel_handler.voxel_world_pos) and voxel_handler.world.crack_pos:
                    voxel_handler.world.crack_pos = glm.ivec3(voxel_handler.voxel_world_pos)
                    voxel_handler.world.acrack_index = 5
                    self.app.sound.playsound(f"minecraft.blocks.{block_name}.dig")
                    
                
                if voxel_handler.world.crack_pos == None  and voxel_handler.voxel_id:

                    voxel_handler.world.crack_pos = glm.ivec3(voxel_handler.voxel_world_pos)
                    voxel_handler.world.acrack_index = 5
                    voxel_handler.rebuild_chunk(*(glm.ivec3(voxel_handler.voxel_world_pos) // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)))
                    voxel_handler.rebuild_adj_chunks((glm.ivec3(voxel_handler.voxel_world_pos) // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)), glm.ivec3(voxel_handler.voxel_world_pos))
                    self.app.sound.playsound(f"minecraft.blocks.{block_name}.dig")
                    
                elif voxel_handler.world.acrack_index != None:
                    
                    
                    voxel_handler.world.acrack_index -= 1
                    voxel_handler.rebuild_chunk(*(glm.ivec3(voxel_handler.voxel_world_pos) // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)))
                    voxel_handler.rebuild_adj_chunks((glm.ivec3(voxel_handler.voxel_world_pos) // glm.ivec3(CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)), glm.ivec3(voxel_handler.voxel_world_pos))
                    
                    if voxel_handler.world.acrack_index <= 0:
                        self.app.sound.playsound(f"minecraft.blocks.{block_name}.destroy")
                    
                        
                      

                        voxel_id = int(voxel_handler.voxel_id)
                        succes = voxel_handler.setblock(*voxel_handler.voxel_world_pos, 0)
                        voxel_handler.world.acrack_index = None
                        voxel_handler.world.crack_pos = None
      
                        voxel_handler.update()
                        if succes:
                            if not to_surival_mined(voxel_id, self.held_item.item_id if self.held_item else 0) == 0:
                                
                              

                                #update inventory
                                for index, value in enumerate(self.inventory.get_normal_use_group(), 1):

                           
                                    if isinstance(value, Item) and value.count < 64 and value.item_id == to_surival_mined(voxel_id, self.held_item.item_id if self.held_item else 0):
                                        value.count += 1
                                        break
                                    elif value == 0:
                                        self.inventory[f'a{index}'] = Item(to_surival_mined(voxel_id, self.held_item.item_id if self.held_item else 0), 1)
                                        break

                    else:
                        self.app.sound.playsound(f"minecraft.blocks.{block_name}.dig")
                        
                
            voxel_handler.update()
            self.hand_angle_rel = 5 if GAMEMODE == CREATIVE else get_dig_time(self.held_item.item_id if self.held_item else 0, voxel_handler.voxel_id) if GAMEMODE == SURIVAL  else 0 




        self.last_lbutton_state = l
        self.last_rbutton_state = r


            
            


        return
    

    def at_death(self):
        
    
        self.on = False
        self.bubbeles = 10
        self.inventory.slots = [0 for i in range(40)]
        if not DIFFICULTY == HARDCORE:
            self.dead = True
        else:
            self.hardcore_death = True
            self.dead = True
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
    


    def damage(self, hp, is_void_damage=False, damage_content=["attack", "chicken"]):
        print(damage_content)
        if GAMEMODE ==  CREATIVE:
            return
        if self.health - hp > 0:
            self.health -= hp
            if hp > 0:
                self.app.sound.playsound("minecraft.entities.player_hurt")
                self.rotate_pitch(0.1 * math.pi)
                self.rotate_yaw(0.15 * math.pi)

                def rotate_back():
                    self.rotate_pitch(-0.15 * math.pi)
                    self.rotate_yaw(-0.2 * math.pi)

                self.app.event_handler.add_task("player_function", rotate_back, time_arg = 0.1)
        else: 
            self.health = 0
            self.app.sound.playsound("minecraft.entities.player_die_sound")
            death_text = ""

            if damage_content[0] == "attack":
                if len(damage_content) == 2:
                    death_text = f"{self.name} was slain by a {damage_content[1]}"
                elif len(damage_content) > 2:
                    death_text = f"{self.name} died in a fight with {" ".join(damage_content[1:-1])} and {damage_content[-1]}"
            elif damage_content[0] == "fall_damage":
                death_text = f"{self.name} died due to fall damage"
            elif damage_content[0] == "drown":
                death_text = f"{self.name} drowned" 
            elif is_void_damage:
                death_text = f"{self.name} fell out off the world"
            elif damage_content[0] == "wither":
                death_text = f"{self.name} withered away"
            self.app.chat.add_messadge("game", death_text.capitalize() + ".")
            self.at_death()

        
    def handle_gravity(self):
        if not self.in_water:
            

            if self.app.collisions.player_collided_bottom(self.position) and self.velocity < 0:
                #fall damage
                if -self.velocity > 1.5:

                    damage = int(-self.velocity * 3.5)
                    print(self.velocity)
                    if not self.can_ud(): self.damage(damage, damage_content=["fall_damage",])
                    
                self.velocity = 0

            elif self.app.collisions.player_collided_top(self.position) and self.velocity > 0:
                self.velocity = 0


            elif not self.app.collisions.player_collided_bottom(self.position) and self.velocity == 0:
                self.velocity = self.vaf + (0.19 if self.app.voxel_handler.getblock(int(self.position.x), int(self.position.y - 1), int(self.position.z)) == WATER_FULL or self.app.voxel_handler.getblock(int(self.position.x), int(self.position.y - 2), int(self.position.z)) == WATER_FULL else 0)


            if self.velocity != 0:
                self.position += glm.vec3(0, self.velocity, 0) 
                self.velocity -= self.gravity


            self.last_vel = self.velocity
        else:
            if not self.app.collisions.player_collided_bottom(self.position) and not pg.key.get_pressed()[pg.K_SPACE]:
                self.position.y -= 0.27

        

    def keyboard_controll(self):
        key_state = pg.key.get_pressed()
        if key_state[pg.K_r]:
            speed = PLAYER_SPRINT_SPEED
        else:
            speed = PLAYER_SPEED
        vel = speed * self.app.delta_time * 1.1

        if self.on:


            if key_state[pg.K_w]:
                self.move_forward(vel)

            if key_state[pg.K_s]:
                self.move_back(vel)

            if key_state[pg.K_a]:
                self.move_left(vel)

            if key_state[pg.K_d]:
                self.move_right(vel)
           
            

            if not self.can_float:
                    
                if key_state[pg.K_SPACE] and self.not_jumping and self.app.collisions.player_collided_bottom(self.position):
                                #fall damage
                    if -self.velocity > 0.9 and self.velocity < 0:

                        damage = int(-self.velocity * 3.5)
                        if damage: self.damage(damage, damage_content=["fall_damage"])
                        
                

                    self.velocity = self.vaj
                    self.not_jumping = False

                elif not key_state[pg.K_SPACE]:
                    self.not_jumping = True
            else:
                if self.in_water and key_state[pg.K_SPACE] and not self.app.collisions.player_collided_top(self.position):
                    self.position.y += 0.22
                elif not self.in_water and key_state[pg.K_SPACE] and not self.app.collisions.player_collided_top(self.position):
                    self.position.y += 1
            



          
        if key_state[pg.K_i] and self._inventory_toggled == False and self.on == True:
            if self.inventory.enabled:
                self.inventory_off() 
            else:
                self.inventory_on()

            self._inventory_toggled = True
        elif not key_state[pg.K_i] and self._inventory_toggled == True:
            self._inventory_toggled = False


        for i in range(1, 9):
            if key_state[eval(f"pg.K_{i}")]:
                self.hand_index = i - 1
                break
   
    def as_entity(self):
        return player_entity(self.app, self.name, self)
    
    def get(self, key):
        if key == "position":
            return self.position
        
        elif key == "x":
            return int(self.position.x)
        elif key == "y":
            return int(self.position.x)
        elif key == "z":
            return int(self.position.x)
        elif key == "inventory":
            return self.inventory
        
        
        else:
            return None

    def set(self, key, value):
        if key == "position":
            self.position = value
        elif key == "x":
            self.position.x = value

        elif key == "y":
            self.position.y = value

        elif key == "z":
            self.position.z = value

      
    def has(self, key):
        if key in ["position", "x", "y", "z", "inventory"]:
            return True
        
        else:
            return False


