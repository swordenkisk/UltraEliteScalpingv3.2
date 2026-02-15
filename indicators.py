"""
ultra_elite_scalping/core/indicators.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Technical indicator calculation engine (12 indicators).
          In production swap random generation for a live price-feed adapter
          (e.g. Alpha Vantage, OANDA, Interactive Brokers).
"""

import random
from typing import Any


class IndicatorEngine:
    """
    Simulates 12 technical indicators per currency pair.

    Pairs supplied externally via ``prices`` dict so state is fully managed
    by the caller (UltraEliteBot).

    Indicators
    ----------
    RSI, Stochastic, CCI, MACD, EMA-fast, EMA-slow, ADX,
    Volume, ATR, Bollinger Band position, Momentum, VWAP-delta
    """

    # ── Signal-biased pools for demo mode ────────────────────────────────────
    _RSI_POOL   = [12, 18, 25, 78, 82, 88]
    _STOCH_POOL = [8, 12, 15, 85, 88, 92]
    _CCI_POOL   = [-185, -170, -145, 140, 165, 185]
    _ADX_POOL   = [28, 32, 35, 38, 42]
    _MACD_POOL  = [0.0018, 0.0022, -0.0017, -0.0020]

    def compute(self, symbol: str, prices: dict[str, float]) -> dict[str, Any]:
        """
        Return a dict of indicator values for *symbol*.
        Updates ``prices[symbol]`` in-place to simulate price movement.
        """
        base = prices[symbol]
        volatility = random.uniform(0.001, 0.0025)
        prices[symbol] = base + random.uniform(-volatility, volatility)
        price = prices[symbol]

        rsi   = random.choice(self._RSI_POOL) + random.uniform(-2,  2)
        stoch = random.choice(self._STOCH_POOL) + random.uniform(-3,  3)
        cci   = random.choice(self._CCI_POOL) + random.uniform(-15, 15)
        macd  = random.choice(self._MACD_POOL) + random.uniform(-0.0001, 0.0001)

        ema_fast = price + random.uniform(-0.0015, 0.0015)
        ema_slow = price + random.uniform(-0.003,  0.003)
        adx      = random.choice(self._ADX_POOL)
        volume   = random.uniform(1.8, 3.2)
        atr      = random.uniform(0.0018, 0.0032)

        # Extra indicators (new in v3.2)
        bb_pos    = random.uniform(-2.0, 2.0)   # Bollinger Band z-score
        momentum  = random.uniform(-1.0, 1.0)   # 10-bar price momentum normalised
        vwap_diff = random.uniform(-0.002, 0.002)

        return {
            "price":    round(price,    5),
            "rsi":      round(rsi,      1),
            "stoch":    round(stoch,    1),
            "cci":      round(cci,      0),
            "macd":     round(macd,     5),
            "ema_fast": round(ema_fast, 5),
            "ema_slow": round(ema_slow, 5),
            "adx":      round(adx,      1),
            "volume":   round(volume,   2),
            "atr":      round(atr,      5),
            "bb_pos":   round(bb_pos,   2),
            "momentum": round(momentum, 3),
            "vwap_diff":round(vwap_diff,5),
        }
