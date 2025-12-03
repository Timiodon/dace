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


def get_sdfg0() -> tuple[str, dict, str, str]:
    sdfg_file = os.path.join(BASE_DIR, "test_sdfgs", "stage1.sdfgz")
    sdfg = SDFG.from_file(sdfg_file)

    from dace.transformation.interstate import LoopToMap

    g = SDFG.from_file('stage1.sdfgz')
    g.validate()

    g.save('stage2-before.sdfgz', compress=True)
    g.apply_transformations(LoopToMap, validate=False)
    g.save('stage2-after.sdfgz', compress=True)
    g.validate()

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


    commit = "5235105e6696f54a09d6420f1c15fbcb0de04390"
    return sdfg, args, commit