"""Run a reproducible Colonel Blotto strategy simulation."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from collections.abc import Sequence
from typing import Literal

BATTLEFIELDS = 10
TOTAL_UNITS = 100
DEFAULT_STRATEGY = (0, 0, 0, 0, 0, 33, 33, 33, 1, 0)
Winner = Literal["strategy", "opponent", "draw"]


def validate_allocation(allocation: Sequence[int]) -> tuple[int, ...]:
    """Return a validated immutable allocation."""
    if len(allocation) != BATTLEFIELDS:
        raise ValueError(f"an allocation must contain {BATTLEFIELDS} values")
    if any(type(value) is not int or value < 0 for value in allocation):
        raise ValueError("allocation values must be non-negative integers")
    if sum(allocation) != TOTAL_UNITS:
        raise ValueError(f"an allocation must use exactly {TOTAL_UNITS} units")
    return tuple(allocation)


def random_allocation(rng: random.Random) -> tuple[int, ...]:
    """Sample uniformly from all non-negative allocations of 100 units."""
    bars = sorted(rng.sample(range(TOTAL_UNITS + BATTLEFIELDS - 1), BATTLEFIELDS - 1))
    boundaries = (-1, *bars, TOTAL_UNITS + BATTLEFIELDS - 1)
    return tuple(boundaries[index + 1] - boundaries[index] - 1 for index in range(BATTLEFIELDS))


def has_three_consecutive_wins(left: Sequence[int], right: Sequence[int]) -> bool:
    return any(
        all(left[index + offset] > right[index + offset] for offset in range(3))
        for index in range(BATTLEFIELDS - 2)
    )


def weighted_score(left: Sequence[int], right: Sequence[int]) -> int:
    """Score battlefields won, with later battlefields worth more."""
    return sum(index for index, (left_units, right_units) in enumerate(zip(left, right), 1) if left_units > right_units)


def determine_winner(strategy: Sequence[int], opponent: Sequence[int]) -> Winner:
    """Apply the streak rule, then use weighted battlefield points as a tiebreak."""
    strategy = validate_allocation(strategy)
    opponent = validate_allocation(opponent)
    strategy_streak = has_three_consecutive_wins(strategy, opponent)
    opponent_streak = has_three_consecutive_wins(opponent, strategy)

    if strategy_streak != opponent_streak:
        return "strategy" if strategy_streak else "opponent"

    strategy_score = weighted_score(strategy, opponent)
    opponent_score = weighted_score(opponent, strategy)
    if strategy_score == opponent_score:
        return "draw"
    return "strategy" if strategy_score > opponent_score else "opponent"


def simulate(strategy: Sequence[int], runs: int = 10_000, seed: int | None = 42) -> dict[str, int]:
    """Evaluate a strategy against uniformly sampled valid allocations."""
    strategy = validate_allocation(strategy)
    if runs < 1:
        raise ValueError("runs must be at least 1")

    rng = random.Random(seed)
    outcomes = Counter(determine_winner(strategy, random_allocation(rng)) for _ in range(runs))
    return {outcome: outcomes[outcome] for outcome in ("strategy", "opponent", "draw")}


def parse_strategy(value: str) -> tuple[int, ...]:
    try:
        return validate_allocation(tuple(int(part.strip()) for part in value.split(",")))
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strategy",
        type=parse_strategy,
        default=DEFAULT_STRATEGY,
        help="ten comma-separated non-negative integers totalling 100",
    )
    parser.add_argument("--runs", type=int, default=10_000, help="number of simulated opponents")
    parser.add_argument("--seed", type=int, default=42, help="random seed for reproducible runs")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    try:
        outcomes = simulate(arguments.strategy, arguments.runs, arguments.seed)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    payload = {
        "strategy": list(arguments.strategy),
        "runs": arguments.runs,
        "seed": arguments.seed,
        "outcomes": outcomes,
        "win_rate": outcomes["strategy"] / arguments.runs,
    }
    if arguments.json:
        print(json.dumps(payload, indent=2))
        return

    print(f"Strategy: {list(arguments.strategy)}")
    print(f"Runs: {arguments.runs:,} (seed {arguments.seed})")
    print(f"Strategy wins: {outcomes['strategy']:,} ({payload['win_rate']:.1%})")
    print(f"Opponent wins: {outcomes['opponent']:,}")
    print(f"Draws: {outcomes['draw']:,}")


if __name__ == "__main__":
    main()
