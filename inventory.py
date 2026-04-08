from settings import *
import pygame as pg
from world_objects.item import InventoryItem as Item
from textures import get_number_surface





def load_icon(name):
    icon = pg.image.load(f"C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\{name}.png")
    icon = pg.transform.scale(icon, (50, 53))
    return icon
class Inventory:
    def __init__(self, app):
        self.app = app
        self.slots = [0 for i in range(40)]

        self.aaa= 0

     
        self.inventory_image = pg.image.load("C:\\Users\\stano\\vs_code\\assets\\inventory.png")
        self.inventory_image = pg.transform.scale(self.inventory_image, (630, 603))


        self.sx = (int(WIN_RES.x) - self.inventory_image.get_width()) // 2
        self.sy = (int(WIN_RES.y) - self.inventory_image.get_height()) // 2
        


        self.item_name_font = pg.font.Font("freesansbold.ttf", 30)
        self.item_names = {SAND:"sand", GRASS:"grass", DIRT:"dirt", STONE:"stone", SNOW:"snow", LEAVES:"leaves", WOOD:"wood", BEDROCK:"bedrock", COMMAND_BLOCK:"command_block", COAL_ORE:"coal_ore", YELLOW_WOOL:"yellow_wool", BLUE_WOOL:"blue_wool", COAL:"coal"}



        self.items = {idx:load_icon(name) for idx,name in self.item_names.items()}


        self.enabled = False

        self.grabbed_item = None
        self.grabbed_item_idf = None
    def idf_to_pos(self, idf):
        if idf == "e":
            return (552, 118)
        
        if len(idf) != 2:
            return None
        
        row, column = idf[0], idf[1]
        x,y = 0,0


        if row in ["a", "b", "c", "d"]:
            if row == "a": y = 520
            elif row == "b": y = 452
            elif row == "c": y = 390
            elif row == "d": y = 330

            if column == "1": x = 23
            elif column == "2": x = 83
            elif column == "3": x = 142
            elif column == "4": x = 200
            elif column == "5": x = 258
            elif column == "6": x = 318
            elif column == "7": x = 376
            elif column == "8": x = 435
            else:
                return None
        elif row == "e":
            if column == "1": x,y = 377, 82
            elif column == "2":x,y = 434, 82
            elif column == "3":x,y = 434, 142
            elif column == "4":x,y = 377,142
            else:
                return None

        elif row == "f":
            x = 23
            if column == "1": y = 23
            elif column == "2": y = 82
            elif column == "3": y = 140
            elif column == "4": y = 199
            else:
                return None
            
            


        return (x + self.sx, y + self.sy)

    def pos_to_idf(self, mx, my):
      
        mx -= self.sx
        my -= self.sy

        if mx > 629 or mx <=0 or my > 600 or my <= 0:
            return None
        
        row = ""
        column = ""

        if mx > 23 and mx < 487 and my > 520 and my < 574:
            row = "a"
        elif mx > 23 and mx < 487 and my > 452 and my < 500:
            row = "b"
        elif mx > 23 and mx < 487 and my > 390 and my < 443:
            row = "c"
        elif mx > 23 and mx < 487 and my > 330 and my < 383:
            row = "d"
        elif mx > 376 and mx < 487 and my > 81 and my < 194:
            row = "e"
        elif mx > 552 and mx < 604 and my > 118 and my < 168:
            return "e"
        elif mx > 24 and mx < 78 and my > 24 and my < 252:
            row = "f"

        else:
            return None
        


        if row in ["a", "b", "c", "d"]:
            if mx > 23 and mx < 78:
                column = 1
            elif mx > 83 and mx < 137:
                column = 2
            elif mx > 142 and mx < 196:
                column = 3
            elif mx > 200 and mx < 253:
                column = 4
            elif mx > 258 and mx < 312:
                column = 5
            elif mx > 318 and mx < 371:
                column = 6
            elif mx >  376 and mx < 429:
                column = 7
            elif mx > 435 and mx < 489:
                column = 8
            else:
                return None
        elif row == "e":
            if mx > 377 and mx < 431 and my > 82 and my < 135:
                column = 1
            elif mx > 434 and mx < 487 and my > 82 and my < 135:
                column = 2
            elif mx > 434 and mx < 487 and my > 142 and my < 192:
                column = 3
            elif mx > 377 and mx < 431 and my > 140 and my < 194:
                column = 4
        elif row == "f":
            if my >  23 and my < 79:
                column = 1
            elif my > 82 and my < 136:
                column = 2
            elif my >  140 and my < 196:
                column = 3
            elif my > 199 and my < 253:
                column = 4
        
        
        
        
        return row + str(column)
        
    def update(self):
        for index, value in enumerate(self.slots):
            if isinstance(value, Item) and value.count == 0:
                self.slots[index] = 0
        if self.enabled:


            l,m, r = pg.mouse.get_pressed()        
          

        #print(self.pos_t_idf(*pg.mouse.get_pos()))
        # if pg.key.get_pressed()[pg.K_c]:

        #     with open("this.txt", "a") as f:
        #         x,y = pg.mouse.get_pos()
        #         f.write(f"{self.aaa} {x - self.sx, y - self.sy}\n")
        #     self.aaa += 1
    def render_hotbar(self):
        for i in range(1, 9):
            idf = f"a{i}"
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            
            try:
                ix,iy = (WIN_RES.x - 423) // 2 + (i-1) * 60, int(WIN_RES.y * 0.80034) + 41
                self.app.scene.render_on_screen(self.items[item_id], ix, iy)        
               
        
            except:
                pass        
        for i in range(1, 9):
            idf = f"a{i}"
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            item_count = self[idf].count if isinstance(self[idf], Item) else 0
            try:
                ix,iy = (WIN_RES.x - 423) // 2 + (i-1) * 60, int(WIN_RES.y * 0.80034) + 41
                ns = get_number_surface(item_count)
                if ns:
                    self.app.scene.render_on_screen(ns, ix + 30, iy + 30)


        
            except:
                pass



    def render(self):
        if not self.enabled:
            return
        screen = pg.surface.Surface(tuple(WIN_RES))
        screen.fill((0, 0, 0))

        screen.blit(self.inventory_image, (self.sx,self.sy))

        slot_idf = [f"a{i + 1}" for i in range(8)] + [f"b{i + 1}" for i in range(8)] + [f"c{i + 1}" for i in range(8)] + [f"d{i + 1}" for i in range(8)] + [f"e{i + 1}" for i in range(4)] + [f"f{i + 1}" for i in range(4)]
        for idf in slot_idf:
        
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            

            if item_id == 0:
                continue

            if self.idf_to_pos(idf):
                x,y = self.idf_to_pos(idf)
            else:
                x,y = 0, 0
          
            try:
                screen.blit(self.items[item_id], (x + 2, y + 2))

                if self.pos_to_idf(*pg.mouse.get_pos()) == idf:
                    text = self.item_name_font.render(self.item_names[item_id], False, "light blue", "dark blue")
                    screen.blit(text, (x + 45, y + 60))
            except:
                pass
        for idf in slot_idf:
        
            item_count = self[idf].count if isinstance(self[idf], Item) else 0
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            
            

            if item_id == 0:
                continue

            if self.idf_to_pos(idf):
                x,y = self.idf_to_pos(idf)
            else:
                x,y = 0, 0
          
            try:
                ns = get_number_surface(item_count)
                if ns:
                    screen.blit(ns, (x + 30, y + 30))


            except:
                pass


        self.app.scene.render_on_screen(screen, 0, 0)

        




    def __setitem__(self, key, value):
        index = self._idf_to_index(key)
        if value:
            self.slots[index] = value
    def __getitem__(self, key):
        index = self._idf_to_index(key)
        return self.slots[index]
    def __delitem__(self, key):
        index = self._idf_to_index(key)
        self.slots[index] = 0   
    def _get_group(self, group_id):
        group_start, group_end = tuple(group_id.split("-"))
        index1 = self._idf_to_index(group_start)
        index2 = self._idf_to_index(group_end) + 1

        return self.slots[index1:index2]
    
    def get_hand_group(self):
        return self._get_group("a1-a8")
    
    def get_craft_group(self):
        return self._get_group("e1-e4")
    
    def get_armor_group(self):
        return self._get_group("f1-f4")
    def get_inventory_group(self):
        return self._get_group("b1-d8")
    def get_normal_use_group(self):
        return self._get_group("a1-d8")
        
    @staticmethod
    def _idf_to_index(idf):
        if type(idf) != str:
            raise TypeError(f"argument 1(idf) must be a string got '{type(idf).__name__}'")
        if len(idf) != 2:
            raise TypeError(f"argument 1(idf) needs to have lentgh '2' got '{len(idf)}'")
        
        row_id, colum = tuple(idf)


        if not colum.isdigit() or not row_id.isalpha() or colum == "0":
            raise TypeError(f"argument 1(idf) has invalid format ('{idf}') should be like a1")


        rows = {"a":0, "b":8, "c":16, "d":24, "e":32, "f":36} # a = hand, b = inventory 1, c = inventory 2, d = inventory 3, e = craftingtable, f = armor
        colum = int(colum) - 1

        index = rows[row_id] + colum
        if index < 40 and index > -1: return index


        raise ValueError(f"bad index '{index}'")



