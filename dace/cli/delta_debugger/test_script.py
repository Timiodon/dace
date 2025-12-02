import numpy as np
import dace
M = dace.symbol("M")
N = dace.symbol("N")

@dace.program
def compute_cell_area(cell_area: dace.float64[M, N], vert: dace.float64[M+1, N+1, 2]):
    """
    Compute cell_areas according to coordinates of vertices
    cell_area: double[M, N], matrix of cell area
    vert: double[M+1, N+1, 2], matrix of vertices
    """
    for i in range(M):
        for j in range(N):
            vertul = vert[i, j, :]
            vertur = vert[i, j+1, :]
            vertbl = vert[i+1, j, :]
            vertbr = vert[i+1, j+1, :]
            area = 0.5*(vertul[1]*vertur[0]-vertul[0]*vertur[1]
                       +vertur[1]*vertbr[0]-vertur[0]*vertbr[1]
                       +vertbr[1]*vertbl[0]-vertbr[0]*vertbl[1]
                       +vertbl[1]*vertul[0]-vertbl[0]*vertul[1])
            cell_area[i, j] = np.abs(area)

M = 40
N = 40
x_range = (0., 1.)
y_range = (0., 1.)
x = np.linspace(*x_range, M+1)
y = np.linspace(*y_range, N+1)
cell_area = np.zeros((M, N))
vert = np.stack(np.meshgrid(x, y, indexing="ij"), axis=-1)
compute_cell_area(cell_area, vert)