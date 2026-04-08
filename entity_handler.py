from settings import *
from typing import Literal
from world_objects.entity import Chicken, player_entity
from terrian_gen import get_height
from utils import get_distance

_gch_type = Literal['a', 'e', 'b']
class EntityHandler:
    def __init__(self, app):
        self.app = app
        self.entities = [self.app.player.as_entity(), ]
        self.block_entities = []
   
    def entity_at(self, position):
        position = glm.ivec3(position)
        entities_at_pos = list(map(lambda entity: entity if glm.ivec3(entity.x, entity.y, entity.z) == position else None, self.entities))
        if entities_at_pos.count(None) != len(entities_at_pos):
            entities_at_pos = list(filter(lambda e: e, entities_at_pos))
            return True, entities_at_pos[0]
        return False, None

    def delte_entity(self, entity_index):
        try:
            del self.entities[entity_index]
        except:
            pass
    def update(self):
        dc = 0
        for index, entity in enumerate(self.entities): 
            if ((hasattr(entity, "_is_garbage") and entity._is_garbage == True) or entity.y < -25) and dc < 8:
                if not isinstance(entity, player_entity):
                    self.delte_entity(index)
                else:
                    entity.kill()
                    self.delte_entity(index)
                    
                dc += 1
            if entity.y < -2:
                entity.damage(2, is_void_damage=True)

            entity.update()
            

        if random.random() < 0.5:
            x,z = random.randint(0, WORLD_W * CHUNK_SIZE), random.randint(0, WORLD_D * CHUNK_SIZE)
            y  = get_height(x, z)
            if get_distance((x, y, z), self.app.player.position) < 90 :
                self.add_e(Chicken(self.app, x, y + 1, z, random.choice(["Chicky", "Chicken", "Chickoletta"])))
    def render(self):
        for i in self.entities: i.render()
    def add_be(self, e):
        self.block_entities.append(e)
    def add_e(self, e):
        self.entities.append(e)
    
    def get_from_gch(self, gch:_gch_type):
        if gch == "a":
            f = list(map(lambda e: e if e.type == "player" else None, self.entities))
            b = f
            for index, value in enumerate(f):
                if value == None:
                    del b[index]
            return b
        if gch == "e":
            return self.entities
        
        if gch == "b":
            return self.block_entities

    def get_from_gche(self,gche:str):
        try:
            if len(gche) < 2: return None
            if gche[0] != "@": return None

            group = self.get_from_gch(gche[1])

            if len(gche) == 2: return group

            if gche[2] != "[": return None
            if gche[-1] != "]": return None

            if gche[-2] != ",":
                gche = gche[:-2] + ",]"

        
            args = {}
            pending = ""
            arg = ""
        

            for index, char in enumerate(gche[3:-1]):
                if char == "=":
                    arg = pending
                    pending = ""

                elif char == "," or index + 1 == len(gche[3:-1]):
                    args[arg] = pending
                    pending = ""


                else: pending += char


            
            


            for index, e in enumerate(group):
                if e:
                    for key, val in args.items():
                        if val.isdigit(): args[key] = int(val)
                        elif val.replace(".", "").isdigit() :args[key] = float(val)
            
                        if e[key] != val:
                            del group[index]
            return group

                        

        except:
            return None

    def get_args(self, gche:str):
        try:
            if len(gche) < 2: return None
            if gche[0] != "@": return None


            if len(gche) == 2: return {}

            if gche[2] != "[": return None
            if gche[-1] != "]": return None


            args:dict[str,str]= {}
            pending = ""
            arg = ""
        

            for index, char in enumerate(gche[3:-1]):
                if char == "=":
                    arg = pending
                    pending = ""

                elif char == "," or index + 1 == len(gche[3:-1]):
                    args[arg] = pending
                    pending = ""


                else: pending += char
            for key, val in args.items():
                if val.isdigit(): args[key] = int(val)
                elif val.replace(".", "").isdigit() :args[key] = float(val)
    
            return args


        except:
            return None

