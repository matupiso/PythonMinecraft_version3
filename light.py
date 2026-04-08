from settings import *

@njit
def propagate_light(light_grid, opacity_grid, sources, max_light=15):
    """
    light_grid: 3D numpy array (uint8) - uchováva intenzitu svetla (0-15)
    opacity_grid: 3D numpy array (bool) - True pre nepriehľadné bloky
    sources: 2D numpy array - zoznam (x, y, z) súradníc svetelných zdrojov
    """
    # Fronta pre BFS (Breadth-First Search)
    # Používame fixnú veľkosť pre Numba kompatibilitu
    queue = np.zeros((light_grid.size, 3), dtype=np.int32)
    head = 0
    tail = 0

    # Inicializácia zdrojov
    for i in range(len(sources)):
        x, y, z = sources[i]
        light_grid[x, y, z] = max_light
        queue[tail] = [x, y, z]
        tail += 1

    # Susedné smery (6-way connectivity)
    adj = np.array([
        [1, 0, 0], [-1, 0, 0],
        [0, 1, 0], [0, -1, 0],
        [0, 0, 1], [0, 0, -1]
    ], dtype=np.int32)

    while head < tail:
        cx, cy, cz = queue[head]
        head += 1
        
        current_val = light_grid[cx, cy, cz]
        if current_val <= 1:
            continue
            
        new_val = current_val - 1

        for i in range(6):
            nx, ny, nz = cx + adj[i, 0], cy + adj[i, 1], cz + adj[i, 2]

            # Kontrola hraníc gridu
            if (0 <= nx < light_grid.shape[0] and 
                0 <= ny < light_grid.shape[1] and 
                0 <= nz < light_grid.shape[2]):
                
                # Šírenie len ak je cieľový blok priehľadný a má nižšie svetlo
                if not opacity_grid[nx, ny, nz] and light_grid[nx, ny, nz] < new_val:
                    light_grid[nx, ny, nz] = new_val
                    queue[tail] = [nx, ny, nz]
                    tail += 1
                    
    return light_grid









lg = np.zeros([10, 10, 10], dtype="uint8")
og = np.random.randint(0,1, size=(10,10,10))

print(propagate_light(lg, og, np.array([[5, 5, 5]]), max_light=5))
print(propagate_light(lg, og, np.array([[5, 5, 5]]), max_light=5))
print(propagate_light(lg, og, np.array([[5, 5, 5]]), max_light=5))
