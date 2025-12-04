import os
import subprocess
import importlib

import sdfgs_for_testing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd):
    subprocess.check_call(cmd, shell=True)
    
def main():

    try:
        pre_fix_commit = "afbcb5f^"
        post_fix_commit = "afbcb5f"

        import dace
        sdfg_file = os.path.join(BASE_DIR, "test_sdfgs", "stage1.sdfgz.txt")
        sdfg = dace.SDFG.from_file(sdfg_file)

        run_cmd(f"git -c advice.detachedHead=false checkout {pre_fix_commit} --recurse-submodules")
        # run_cmd(f"git revert {commit} --no-commit")
        
        importlib.reload(dace)
        from dace.transformation.interstate import LoopToMap
        sdfg.apply_transformations_repeated(LoopToMap, validate=False)
        sdfg.validate()
    except Exception as e:
        print("An error of type", type(e).__name__, "occurred.")
    finally:
        pass
        run_cmd("git checkout delta_debugger --recurse-submodules")
        # run_cmd("git reset --hard")


if __name__ == "__main__":
    main()