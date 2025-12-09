import os
import subprocess
import numpy as np
from dace.sdfg import SDFG
import dace

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_sdfg_old_commit() -> tuple[str, dict, str, str]:
    sdfg_file = os.path.join(BASE_DIR, "test_sdfgs", "program.sdfg")
    sdfg = SDFG.from_file(sdfg_file)

    M = dace.symbol("M")
    N = dace.symbol("N")
    M = 40
    N = 40
    x_range = (0., 1.)
    y_range = (0., 1.)
    x = np.linspace(*x_range, M+1)
    y = np.linspace(*y_range, N+1)
    cell_area = np.zeros((M, N))
    vert = np.stack(np.meshgrid(x, y, indexing="ij"), axis=-1)
    args = {"cell_area": cell_area, "vert": vert, "M": M, "N": N}

    pre_fix_commit = "d8327ab106e727f933053417a35828172f53d530^"
    post_fix_commit = "5235105e6696f54a09d6420f1c15fbcb0de04390"
    return sdfg, args, pre_fix_commit, post_fix_commit


def get_fill_sdfg():
    import dace as dc
    N = dc.symbol('N')

    @dc.program
    def global_matmul(C: dc.float32[N, N] @ dc.StorageType.GPU_Global):
        for i, j in dc.map[0:N:N, 0:N:N] @ dc.ScheduleType.GPU_Device:

            for l in dc.map[0:64] @ dc.ScheduleType.GPU_ThreadBlock:

                c = dc.ndarray(
                    [N, N],
                    dtype=dc.float32,
                    storage=dc.StorageType.Register,
                    strides=(N, 1),
                )

                for k in dc.map[0:1] @ dc.ScheduleType.Sequential:
                    c.fill(0.0)

                C[i:i + N, j:j + N] = c[:, :]

    return global_matmul