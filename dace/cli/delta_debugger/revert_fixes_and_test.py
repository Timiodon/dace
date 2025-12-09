import os
import subprocess
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd):
    subprocess.check_call(cmd, shell=True)

def checkout_commit(commit_hash):
    run_cmd(f"git -c advice.detachedHead=false checkout {commit_hash} --recurse-submodules")
    
def test_loop_to_map():
    pre_fix_commit = "afbcb5f^"
    post_fix_commit = "afbcb5f"

    import dace
    sdfg_file = os.path.join(BASE_DIR, "test_sdfgs", "stage1.sdfgz.txt")
    sdfg = dace.SDFG.from_file(sdfg_file)

    checkout_commit(pre_fix_commit)
    
    importlib.reload(dace)
    from dace.transformation.interstate import LoopToMap
    sdfg.apply_transformations_repeated(LoopToMap, validate=False)
    sdfg.validate()

def test_issue_2100():
    """
    Reproduction of issue #2100, where a nested SDFG with a fill operation
    would not register the filled array as an output, causing a validation failure.
    """
    pre_fix_commit = "21bf47e^"
    post_fix_commit = "21bf47e"
    import dace
    from sdfgs_for_testing import get_fill_sdfg
    checkout_commit(post_fix_commit)

    importlib.reload(dace)
    global_matmul = get_fill_sdfg()

    sdfg = global_matmul.to_sdfg(simplify=False)
    sdfg.validate()
    sdfg.simplify()
    sdfg.validate()
    

def main():
    try:
        test_issue_2100()
        print("No exceptions occurred.")
    except Exception as e:
        print("An error of type", type(e).__name__, "occurred.")
        print(e)
    finally:
        pass
        run_cmd("git checkout delta_debugger --recurse-submodules")

if __name__ == "__main__":
    main()