from settings import *
import re
from world_objects.entity import player_entity
class Rint: 
    def __init__(self, x): self.x = int(x)

cmd_syntax_tree = {
    "setblock": [(1, "<x> <y> <z> <block_name>"),],
    "tp": [(1, "<player> <x> <y> <z> yaw (<yaw>|<intyaw>) pitch (<pitch>|<intpitch>)"),
           (2, "<player> <x> <y> <z> yaw (<yaw>|<intyaw>)"),
           (3, "<player> <x> <y> <z> pitch (<pitch>|<intpitch>)"),
           (4, "<player> <x> <y> <z> pitch (<pitch>|<intpitch>) yaw (<yaw>|<intyaw>)"),
           (5, "<player> <x> <y> <z>"), ], 
}




class Commands:


    def __init__(self, app):
        self.app = app
        self.is_valid_type = {
        "x":self.arg_is_int,
        "y":self.arg_is_int,
        "z":self.arg_is_int,
        "block_name":self.arg_isblocktype,
        "player":self.arg_isplayer,
        "pitch":self.isfloat,
        "intpitch":self.arg_is_int,
        "yaw":self.isfloat,
        "intyaw":self.arg_is_int,
        
        }
        self.decodes = {
            "x":self.decode_intarg,
            "y":self.decode_intarg,
            "z":self.decode_intarg,
            "block_name":self.decode_blockname,
            "player":self.decode_playerarg,
            "intyaw":self.decode_intarg,
            "intpitch":self.decode_intarg,
            "yaw":self.decode_float_arg,
            "pitch":self.decode_float_arg,
        }

        self.commands = {
            "setblock": self.setblock_cmd,
            "tp":self.tp_cmd,
        }
        self.permission_levels = {
            "setblock":[2,],
            "tp":[2,],
        }
    def isfloat(self, x:str):
        if x.count(".") == 1 and x.replace(".", "").isdigit():
            return True
        return False
    def arg_isplayer(self, x:str):
        if x.isalpha() and x in list(map(lambda x: x.name, list(
            filter(lambda x: isinstance(x, player_entity),self.app.entity_handler.entities)))):
            return True
        return False
    def decode_float_arg(self, x:str):
        return float(x)
    def decode_playerarg(self, a):
        return list(filter(lambda x: isinstance(x, player_entity) and x.name == a, self.app.entity_handler.entities))
    def tp_cmd(self, exec_pos, parsed_args, executor_entity, syntax_id):
        ex,ey,ez = exec_pos
        x,y,z =   0, 0, 0

        if isinstance(parsed_args[1], Rint):
            x = ex +  parsed_args[1].x
        else:
            x = parsed_args[1]

        if isinstance(parsed_args[2], Rint):
            y = ey +  parsed_args[2].x
        else:
            y = parsed_args[2]

        if isinstance(parsed_args[3], Rint):
            z = ez +  parsed_args[3].x
        else:
            z = parsed_args[3]


        if syntax_id == 5:
            executor_entity["x"] = x
            executor_entity["y"] = y
            executor_entity["z"] = z
            return "Succesfully teleported entity", True
        
        elif syntax_id == 1 and isinstance(executor_entity, player_entity):
            executor_entity["x"] = x
            executor_entity["y"] = y
            executor_entity["z"] = z

            executor_entity["yaw"] = math.pi * (parsed_args[4] / 180)
            executor_entity["pitch"] = math.pi * (parsed_args[5] / 180)
            return "Succesfully teleported entity", True
        elif syntax_id == 2 and isinstance(executor_entity, player_entity):
            executor_entity["x"] = x
            executor_entity["y"] = y
            executor_entity["z"] = z

            executor_entity["yaw"] = math.pi * (parsed_args[4] / 180)
            return "Succesfully teleported entity", True
        
        elif syntax_id == 3 and isinstance(executor_entity, player_entity):
            executor_entity["x"] = x
            executor_entity["y"] = y
            executor_entity["z"] = z

            executor_entity["pitch"] = math.pi * (parsed_args[4] / 180)
            return "Succesfully teleported entity", True
        
        elif syntax_id == 4 and isinstance(executor_entity, player_entity):
            executor_entity["x"] = x
            executor_entity["y"] = y
            executor_entity["z"] = z

            executor_entity["pitch"] = math.pi * (parsed_args[4] / 180)
            executor_entity["yaw"] = math.pi * (parsed_args[5] / 180)
            return "Succesfully teleported entity", True


    def setblock_cmd(self, exec_pos, parsed_args, executor_entity, syntax_id):
        ex,ey,ez = exec_pos
        x,y,z =   0, 0, 0

        if isinstance(parsed_args[0], Rint):
            x = ex +  parsed_args[0].x
        else:
            x = parsed_args[0]
        
        if isinstance(parsed_args[1], Rint):
            y = ey +  parsed_args[1].x
        else:
            y = parsed_args[1]
        
        if isinstance(parsed_args[1], Rint):
            z = ez +  parsed_args[1].x
        else:
            z = parsed_args[1]

        if x < 0 or x >= WORLD_W * CHUNK_SIZE or y < 0 or y >= WORLD_Y or z < 0 or z >= WORLD_D * CHUNK_SIZE:
            return "The position is out of the world.", False
        

        x,y,z = int(x), int(y), int(z)

        self.app.voxel_handler.setblock(x,y,z,parsed_args[3])        
        return "Succesfully placed a block", True
        
            
    def get_isvalid(self, arg_syntax:str):
        def isvalid_str(strings:list):
            def isvalid(x):
                if x in strings:
                    return True
                return False
            return isvalid
        def isvalid_arg(strings):
           
            def isvalid(x):
                
                for string in strings:
                    a = self.is_valid_type.get(string[1:-1])
                    

                    if not a: continue

                    if a(x):
                        return True
                return False
            return isvalid
            
        if len(arg_syntax) < 3 and arg_syntax.isalpha():
            return isvalid_str([arg_syntax, ])
        if arg_syntax[0] == "(" and arg_syntax[-1] == ")":
            if "<" in arg_syntax:
                return isvalid_arg(arg_syntax[1:-1].split("|"))
            else:
                return isvalid_str(arg_syntax[1:-1].split("|"))
        else:
            if arg_syntax[0] == "<" and arg_syntax[-1] == ">":
                return self.is_valid_type.get(arg_syntax[1:-1])
            else:
                return isvalid_str([arg_syntax,])

    def arg_is_int(self, x:str):
        if x.isdigit() or x == "~" or (len(x) > 1 and x[0] == "~" and x[1:].isdigit()):
            return True
        return False
    def decode_intarg(self, x:str):
        if x.isdigit(): return int(x)
        if x == "~": return Rint(0)
        elif len(x) > 1 and x[0] == "~" and x[1:].isdigit() :return Rint(x[1:])
        return 0
    def decode_blockname(self, x:str):
        if x.upper() in BLOCK_NAMES:
            return BLOCKS[BLOCK_NAMES.index(x.upper())]
        elif x[:10] == "minecraft:" and x[10:].upper() in BLOCK_NAMES:
            return BLOCKS[BLOCK_NAMES.index(x[10:].upper())]
        return 0
    def arg_isblocktype(self, x:str):
        if x.upper() in BLOCK_NAMES or (x[:10] == "minecraft:" and x[10:].upper() in BLOCK_NAMES):
            return True
        return False
    
    def parse(self, command):
        a = re.split(r"\s+", command)
        if len(a) < 2: return "Not enough args.", None, None, None, None
        command = a[0]
        all_syntax = cmd_syntax_tree.get(command)
        if not all_syntax: return "Invalild command.", None, None, None, None
        args = a[1:]

        syntax = ""
        syntax_id = 0


        for s in all_syntax:
            syn_id, syn = s
            syn = re.split(r"\s+", syn)

            if not len(syn) == len(args):
                continue

            
            for index, arg in enumerate(args):
                isvalid = self.get_isvalid(syn[index])

                if not isvalid:
                    continue

                if isvalid(arg):
                    syntax = syn
                    syntax_id = syn_id

                else:
                    syntax = ""
                    syntax_id = 0
                    break
            if syntax_id != 0: 
                break
        
        if syntax_id == 0:
            return "Invalid syntax", None, None, None,None
        

        parsed_args = []
        for index, value in enumerate(args):
            if syntax[index][0] == "<" and syntax[index][-1] == ">":
                parsed_args.append(self.decodes[syntax[index][1:-1]](value))
            else:
                parsed_args.append(value)
        return 1, parsed_args, syntax_id, syntax, command
        
    def execute(self, command_text, exec_entity, exec_pos, permission_level):
        messadge, parsed_args, syntax_id, syntax, command = self.parse(command_text)
        if messadge != 1:
            self.app.chat.add_messadge("game", messadge, color="red")
            return 

        cmd_function = self.commands[command]

        messadge, success = cmd_function(exec_pos=exec_pos, parsed_args=parsed_args,
                                         executor_entity=exec_entity, syntax_id=syntax_id)
        
        
        self.app.chat.add_messadge("game", messadge, color="white" if success else "red")
        


        
        



