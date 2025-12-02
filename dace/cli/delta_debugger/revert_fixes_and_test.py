import os
import subprocess
import numpy as np
from dace.sdfg import SDFG
import dace

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_sdfg_args_commit() -> tuple[str, dict, str]:
    sdfg_file = os.path.join(BASE_DIR, "test_sdfgs", "program.sdfg")

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
    return sdfg_file, args, commit

def run_cmd(cmd):
    subprocess.check_call(cmd, shell=True)
    
def main():

    try:
        sdfg_file, args, commit = get_sdfg_args_commit()
        sdfg = SDFG.from_file(sdfg_file)
        run_cmd(f"git checkout {commit} --recurse-submodules")
        # run_cmd(f"git revert {commit} --no-commit")
        
        sdfg(**args)

    finally:
        run_cmd("git checkout delta_debugger --recurse-submodules")
        # run_cmd("git reset --hard")


if __name__ == "__main__":
    main()