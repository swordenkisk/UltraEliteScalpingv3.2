"""
ultra_elite_scalping/core/scoring.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Deterministic scoring engine.  News sentiment and AI confirmation
          bonuses are applied here so scoring stays testable in isolation.
"""

from dataclasses import dataclass, field
from config.settings import SCORE_WEIGHTS


@dataclass
class ScoreResult:
    buy_score:  int
    sell_score: int
    direction:  str          # "BUY" | "SELL" | "HOLD"
    triggers:   list[str] = field(default_factory=list)


class ScoringEngine:
    """
    Evaluates indicator data and returns a ScoreResult.

    News sentiment and AI confirmation bonuses are passed in as integers
    so this class stays decoupled from external APIs.
    """

    def score(
        self,
        data: dict,
        news_bonus: int = 0,
        ai_bonus: int = 0,
        threshold: int = 65,
    ) -> ScoreResult:
        """
        Parameters
        ----------
        data        : indicator dict from IndicatorEngine.compute()
        news_bonus  : positive = bullish, negative = bearish (−10 to +10)
        ai_bonus    : Claude AI confirmation points (0 to +20)
        threshold   : minimum score to emit a signal

        Returns
        -------
        ScoreResult with buy/sell scores and a human-readable trigger list.
        """
        w = SCORE_WEIGHTS
        buy_score = 0
        sell_score = 0
        triggers: list[str] = []

        # ── Price Action (25 pts) ────────────────────────────────────────────
        if data["price"] > data["ema_fast"]:
            buy_score  += w["price_action"]
            triggers.append("PA↑")
        else:
            sell_score += w["price_action"]
            triggers.append("PA↓")

        # ── RSI Extremes (20 pts) ────────────────────────────────────────────
        if data["rsi"] < 22:
            buy_score  += w["rsi"]
            triggers.append("RSI-OB")
        elif data["rsi"] > 82:
            sell_score += w["rsi"]
            triggers.append("RSI+OS")

        # ── Stochastic (18 pts) ──────────────────────────────────────────────
        if data["stoch"] < 15:
            buy_score  += w["stoch_cci"]
            triggers.append("STOCH-")
        elif data["stoch"] > 88:
            sell_score += w["stoch_cci"]
            triggers.append("STOCH+")

        # ── MACD (15 pts) ────────────────────────────────────────────────────
        if data["macd"] > 0.0015:
            buy_score  += w["macd"]
            triggers.append("MACD+")
        elif data["macd"] < -0.0015:
            sell_score += w["macd"]
            triggers.append("MACD-")

        # ── ADX Trend Strength (12 pts) ──────────────────────────────────────
        if data["adx"] > 30:
            if data["price"] > data["ema_fast"]:
                buy_score  += w["adx"]
            else:
                sell_score += w["adx"]
            triggers.append(f"ADX{data['adx']:.0f}")

        # ── News Sentiment Bonus (±10 pts) ───────────────────────────────────
        if news_bonus > 0:
            buy_score  += news_bonus
            triggers.append(f"NEWS+{news_bonus}")
        elif news_bonus < 0:
            sell_score += abs(news_bonus)
            triggers.append(f"NEWS{news_bonus}")

        # ── Claude AI Confirmation Bonus (0-20 pts) ──────────────────────────
        if ai_bonus > 0:
            if buy_score > sell_score:
                buy_score  += ai_bonus
            else:
                sell_score += ai_bonus
            triggers.append(f"AI+{ai_bonus}")

        # ── Determine direction ──────────────────────────────────────────────
        if buy_score >= threshold and buy_score >= sell_score:
            direction = "BUY"
        elif sell_score >= threshold and sell_score > buy_score:
            direction = "SELL"
        else:
            direction = "HOLD"

        return ScoreResult(
            buy_score=buy_score,
            sell_score=sell_score,
            direction=direction,
            triggers=triggers[:5],
        )
