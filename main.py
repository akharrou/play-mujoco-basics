"""MuJoCo simulation runner.

Usage:
    main.py [--asset PATH] [--headless] [--steps N] [--max-time SECS]
    main.py (-h | --help)

Options:
    --asset PATH       Path to MuJoCo XML asset [default: assets/simple_box.xml]
    --headless         Run without rendering a viewer
    --steps N          Number of simulation steps to run (0 = unlimited until max-time) [default: 0]
    --max-time SECS    Maximum wall-clock seconds to simulate (0 = unlimited) [default: 5.0]
    -h --help          Show this help message
"""

import pathlib
import time

import mujoco
from docopt import docopt


def run_sim(model_path: pathlib.Path, headless: bool, steps: int, max_time: float):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    m = mujoco.MjModel.from_xml_path(str(model_path))
    d = mujoco.MjData(m)

    viewer = None
    if not headless:
        try:
            from mujoco import viewer as mj_viewer
            viewer = mj_viewer.launch_passive(m, d)
        except Exception as e:  # noqa: BLE001
            print(f"Viewer launch failed ({e}); continuing headless.")
            headless = True

    start_wall = time.time()
    step_count = 0
    while True:
        mujoco.mj_step(m, d)
        step_count += 1

        if viewer is not None:
            try:
                viewer.sync()
            except Exception as e:  # noqa: BLE001
                print(f"Viewer sync error, closing: {e}")
                viewer.close()
                viewer = None
                headless = True

        if steps > 0 and step_count >= steps:
            break
        if max_time > 0 and (time.time() - start_wall) >= max_time:
            break

    if viewer is not None:
        viewer.close()

    return step_count


def main():
    args = docopt(__doc__)
    asset = pathlib.Path(args["--asset"]) if args["--asset"] else pathlib.Path("assets/simple_box.xml")
    headless = bool(args["--headless"])  # already True/False
    try:
        steps = int(args["--steps"])
    except ValueError as e:  # noqa: BLE001
        raise SystemExit(f"--steps must be an integer: {e}") from e
    try:
        max_time = float(args["--max-time"])
    except ValueError as e:  # noqa: BLE001
        raise SystemExit(f"--max-time must be a float: {e}") from e

    steps_run = run_sim(asset, headless, steps, max_time)
    print(f"Simulation finished after {steps_run} steps.")
    print(f"Simulation finished after {steps} steps.")


if __name__ == "__main__":  # pragma: no cover
    main()
