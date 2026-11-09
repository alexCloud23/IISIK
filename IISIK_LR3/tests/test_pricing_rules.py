from __future__ import annotations

from decimal import Decimal

import pytest

from shared.errors import InvalidInputError
from shared.pricing_rules import (
    compute_recommended_price,
    compute_recommendation,
    round_money,
)


class TestRoundMoney:
    def test_rounds_half_up(self):
        assert round_money("2.345") == Decimal("2.35")

    def test_keeps_two_digits(self):
        assert round_money(1299) == Decimal("1299.00")


class TestComputeRecommendedPrice:
    def test_match_takes_competitor_price(self):
        assert compute_recommended_price(
            Decimal("1299.00"), "MATCH", Decimal("1249.00")
        ) == Decimal("1249.00")

    def test_undercut_factor(self):
        assert compute_recommended_price(
            Decimal("1299.00"), "UNDERCUT", Decimal("1149.00")
        ) == Decimal("1137.51")

    def test_premium_factor(self):
        assert compute_recommended_price(
            Decimal("1299.00"), "PREMIUM"
        ) == Decimal("1324.98")

    def test_no_strategy_keeps_price(self):
        assert compute_recommended_price(Decimal("1299.00")) == Decimal("1299.00")

    def test_price_below_cost_falls_back_to_current(self):
        assert compute_recommended_price(
            Decimal("100.00"), "MATCH", Decimal("50.00")
        ) == Decimal("100.00")


class TestComputeRecommendation:
    def test_unknown_strategy_raises(self):
        with pytest.raises(InvalidInputError):
            compute_recommendation(Decimal("1299.00"), "AGGRESSIVE", Decimal("999"))

    def test_match_without_competitor_price_raises(self):
        with pytest.raises(InvalidInputError):
            compute_recommendation(Decimal("1299.00"), "MATCH", None)

    def test_reason_with_strategy(self):
        _, reason = compute_recommendation(
            Decimal("1299.00"), "UNDERCUT", Decimal("1149.00"), Decimal("46.00")
        )
        assert "UNDERCUT" in reason
        assert "1149.00 BYN" in reason
        assert "46.00 ед." in reason
        assert "1137.51 BYN" in reason

    def test_reason_without_strategy(self):
        _, reason = compute_recommendation(
            Decimal("1299.00"), None, None, Decimal("46.00")
        )
        assert "без изменений" in reason

    def test_reason_for_cost_floor(self):
        _, reason = compute_recommendation(
            Decimal("100.00"), "MATCH", Decimal("50.00"), Decimal("10.00")
        )
        assert "ниже себестоимости" in reason
