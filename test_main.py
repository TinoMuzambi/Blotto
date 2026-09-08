import random
import unittest

from main import (
    DEFAULT_STRATEGY,
    determine_winner,
    has_three_consecutive_wins,
    random_allocation,
    simulate,
    validate_allocation,
)


class BlottoTests(unittest.TestCase):
    def test_random_allocations_are_valid_and_reproducible(self) -> None:
        first = random_allocation(random.Random(7))
        second = random_allocation(random.Random(7))
        self.assertEqual(first, second)
        self.assertEqual(sum(first), 100)
        self.assertEqual(len(first), 10)
        self.assertTrue(all(value >= 0 for value in first))

    def test_invalid_allocations_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_allocation((100,))
        with self.assertRaises(ValueError):
            validate_allocation((10,) * 9 + (9,))
        with self.assertRaises(ValueError):
            validate_allocation((10,) * 9 + (-1,))

    def test_consecutive_rule_checks_every_window(self) -> None:
        left = (0, 0, 0, 0, 0, 30, 30, 30, 10, 0)
        right = (10, 10, 10, 10, 10, 0, 0, 0, 40, 10)
        self.assertTrue(has_three_consecutive_wins(left, right))

    def test_streak_wins_before_weighted_score(self) -> None:
        strategy = (34, 33, 33, 0, 0, 0, 0, 0, 0, 0)
        opponent = (0, 0, 0, 0, 0, 0, 0, 0, 0, 100)
        self.assertEqual(determine_winner(strategy, opponent), "strategy")

    def test_simulation_is_seeded_and_counts_every_run(self) -> None:
        first = simulate(DEFAULT_STRATEGY, runs=250, seed=11)
        self.assertEqual(first, simulate(DEFAULT_STRATEGY, runs=250, seed=11))
        self.assertEqual(sum(first.values()), 250)


if __name__ == "__main__":
    unittest.main()
