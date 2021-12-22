import cocotb
import random
# All testbenches use tinyalu_utils, so store it in a central
# place and add its path to the sys path so we can import it
import sys
from pathlib import Path
sys.path.append(str(Path("..").resolve()))
from tinyalu_utils import TinyAluBfm, Ops, alu_prediction, logger  # noqa: E402


# ## The cocotb test

@cocotb.test()
async def test_alu(_):
    """Test all TinyALU Operations"""
    passed = True
    bfm = TinyAluBfm()
    await bfm.reset()
    bfm.start_tasks()
# ### Sending commands
    cvg = set()
    ops = list(Ops)
    for op in ops:
        aa = random.randint(0, 255)
        bb = random.randint(0, 255)
        await bfm.send_op(aa, bb, op)
# ### Monitoring commands
        seen_cmd = await bfm.get_cmd()
        seen_op = Ops(seen_cmd[2])
        cvg.add(seen_op)
        result = await bfm.get_result()
        pr = alu_prediction(aa, bb, op)
        if result == pr:
            logger.info(f"PASSED: {aa:02x} {op.name} {bb:02x} = {result:04x}")
        else:
            logger.error(f"FAILED: {aa:02x} {op.name} {bb:02x} = "
                         f"{result:04x} - predicted {pr:04x}")
            passed = False
    if len(set(Ops) - cvg) > 0:
        logger.error(f"Functional coverage error. Missed: {set(Ops)-cvg}")
        passed = False
    else:
        logger.info("Covered all operations")
    assert passed
