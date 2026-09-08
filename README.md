# Colonel Blotto simulator

A small, dependency-free Python simulator for evaluating a fixed allocation in a
10-battlefield Colonel Blotto variant. Each player allocates exactly 100 units.
A unique run of three consecutive battlefield wins decides the game; otherwise,
won battlefields score their one-based position and the higher total wins.

The opponent generator samples valid non-negative allocations rather than the
order-biased, sometimes incomplete allocations used by the original script.
Runs are deterministic by default, making experiments and regressions repeatable.

## Run it

```bash
python main.py
python main.py --runs 50000 --seed 7
python main.py --strategy 34,33,33,0,0,0,0,0,0,0 --json
```

## Verify it

```bash
python -m unittest -v
python -m compileall -q main.py test_main.py
```

The project targets Python 3.12+ and has no third-party dependencies.
