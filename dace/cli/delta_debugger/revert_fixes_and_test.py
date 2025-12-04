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
    checkout_commit(post_fix_commit)

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