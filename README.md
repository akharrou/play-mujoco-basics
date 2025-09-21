# MuJoCo Quick Start

This minimal project shows how to launch MuJoCo, load an XML asset, and (optionally) open the interactive viewer.

## 1. Install Python dependencies

Create / activate a virtual environment (recommended) and install the project in editable mode or just the deps.

```bash
uv venv --python python3.10 .venv
source .venv/bin/activate  # macOS/Linux
uv pip install --upgrade pip
uv pip install -e .
```

`pyproject.toml` already lists:
- `mujoco`
- `numpy` (for future numerical work)
- `docopt` (for argument parsing)

Validate install:
```bash
python -c "import mujoco; print('MuJoCo version:', mujoco.__version__)"
```

## 2. Run a headless simulation (smoke test)

```bash
mjpython main.py --headless --steps 500
```
You should see: `Simulation finished after 500 steps.`

## 3. Launch with viewer

```bash
mjpython main.py --steps 0 --max-time 10 --asset assets/simple_box.xml
```
Because `--steps 0` means unlimited until `--max-time` (10s by default), or if `--max-time 0` then it runs until you close the viewer window.

If the viewer fails to open (e.g., remote session without GUI), the script will fall back to headless mode and print a warning.

<!--


## 4. Use a different asset

Add or modify XML files in `assets/` and pass via `--asset`:
```bash
mjpython main.py --asset assets/simple_box.xml --max-time 5
```

-->

## 4. Command line arguments (now using docopt)

Use `mjpython main.py --help` to see usage.

<!--

## 6. File overview

| File | Purpose |
|------|---------|
| `main.py` | Loads model, runs simulation loop, optional viewer. Uses docopt for CLI parsing. |
| `assets/simple_box.xml` | Minimal free joint box over a plane. |
| `pyproject.toml` | Project metadata & dependencies. |

## 7. Troubleshooting

Common issues:

- `GLFW error` or viewer fails on headless server: add `--headless` flag or ensure a display (`XQuartz` or `mesa` / `xvfb` for CI). On macOS locally it should just work.
- `FileNotFoundError: assets/simple_box.xml`: run from project root or give an absolute path.
- `mujoco.FatalError: Could not open file`: path typo or missing asset file.

### Verify GPU/Renderer
MuJoCo viewer uses OpenGL. On macOS it relies on the system framework. For software rendering fallback you can try:
```bash
export MUJOCO_GL=osmesa  # or 'egl' if you have proper drivers
```
Then rerun the script headless or with viewer (if supported).

## 8. Next steps

Ideas to extend:
- Add actuators and controls (PID torque application).
- Log states (qpos, qvel) to NumPy arrays and save to `.npy`.
- Add a simple controller that orients the box.
- Integrate with reinforcement learning libraries (Gymnasium wrapper).

-->
