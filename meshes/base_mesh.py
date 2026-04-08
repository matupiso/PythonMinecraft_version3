import numpy as np
import moderngl_window as mglw




class BaseMesh:
    def __init__(self):
        #moderngl context
        self.ctx = None

        #shader program
        self.program = None

        #vertex buffer data type
        self.vbo_format = None

        #attribute names according to vbo_format
        self.attrs: tuple[str, ...] = None

        #vertex array object
        self.vao = None

    def get_vertex_data(self) -> np.array: ...


    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )

        return vao
    
    def render(self):
        self.vao.render()

def load_model(model_name):
    def add_point(point, array):
        array.append(point[0])
        array.append(point[1])
        array.append(point[2])
        return array
        
    with open(f"assets\\models\\{model_name}.obj", 'r') as file:
        contents = file.read()

    ind = 1
    pts = {}
    data = []

    for line in contents.split("\n"):
        parts = line.split(" ")
        if parts[0] == "v":
            pts[ind] = [float(parts[1]), float(parts[2]), float(parts[3])]
            ind += 1

    for line in contents.split("\n"):
        parts = line.split(" ")
        if parts[0] == "f":
            a,b,c,d = int(parts[1].split("/")[0]), int(parts[2].split("/")[0]), int(parts[3].split("/")[0]), int(parts[4].split("/")[0])
            data = add_point(pts[a], data)
            data = add_point(pts[c], data)
            data = add_point(pts[d], data)
            
            data = add_point(pts[a], data)
            data = add_point(pts[b], data)
            data = add_point(pts[c], data)

      

            

    

    data = np.array(data, dtype="float32")
    return data


            

class MixedBaseMesh:
    def __init__(self):
        #moderngl context
        self.ctx = None

        #shader program
        self.program = None

        #vertex buffer data type
        self.vbo_format = None

        #attribute names according to vbo_format
        self.attrs: tuple[str, ...] = None

        #vertex array object
        self.vao2 = None
        self.vao1 = None

    def get_vertex_data1(self) -> np.array: ...
    def get_vertex_data2(self) -> np.array: ...




    def get_vao1(self):
        vertex_data = self.get_vertex_data1()
        vbo = self.ctx.buffer(vertex_data)
        
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )

        return vao
    def get_vao2(self):
        vertex_data = self.get_vertex_data2()
        vbo = self.ctx.buffer(vertex_data)
        
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )

        return vao
    
    def render1(self):
        self.vao1.render()
    def render2(self):
        self.vao2.render()