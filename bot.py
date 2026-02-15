"""
ultra_elite_scalping/core/bot.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Top-level bot orchestrator.  Wires together:
            - IndicatorEngine  (technical analysis)
            - ScoringEngine    (signal generation)
            - NewsAPIClient    (market news sentiment)
            - AIAnalysisClient (Claude AI confirmation)
            - display helpers  (terminal output)
"""

import time
import math
from config import settings
from core.indicators import IndicatorEngine
from core.scoring    import ScoringEngine
from apis.news_api   import NewsAPIClient
from apis.ai_api     import AIAnalysisClient
import utils.display as ui


class UltraEliteBot:
    """
    Main bot class.

    Lifecycle
    ---------
    1. run_ultra() → infinite loop of 45-second cycles
    2. Each cycle: sweep all 6 pairs via _analyse_pair()
    3. _analyse_pair(): compute indicators → fetch news → ask Claude →
                        score → emit alert if signal found
    """

    def __init__(self) -> None:
        self.prices: dict[str, float] = dict(settings.PAIRS)
        self.signals: int = 0
        self.wins: int = 0
        self.max_score: int = 0

        self._indicators = IndicatorEngine()
        self._scorer     = ScoringEngine()
        self._news       = NewsAPIClient(settings.NEWS_API_KEY)
        self._ai         = AIAnalysisClient(settings.ANTHROPIC_API_KEY)

        # Cache: refreshed every NEWS_REFRESH_CYCLES cycles
        self._cached_headlines: list[dict] = []
        self._news_cycle_counter: int = 0

    # ── Public ────────────────────────────────────────────────────────────────

    def run_ultra(self) -> None:
        """Entry point — runs until KeyboardInterrupt."""
        ui.print_banner()
        cycle = 0
        try:
            while True:
                cycle += 1
                self._refresh_news_if_needed()
                ui.print_cycle_header(cycle)

                cycle_signals = 0
                for symbol in self.prices:
                    if self._analyse_pair(symbol):
                        cycle_signals += 1
                    time.sleep(settings.PAIR_DELAY)

                ui.print_cycle_footer(
                    cycle, cycle_signals,
                    self.signals, self.wins, self.max_score
                )
                self._countdown(cycle)

        except KeyboardInterrupt:
            ui.print_shutdown(self.signals, self.wins)

    # ── Private ───────────────────────────────────────────────────────────────

    def _refresh_news_if_needed(self) -> None:
        self._news_cycle_counter += 1
        if self._news_cycle_counter >= settings.NEWS_REFRESH_CYCLES:
            self._cached_headlines = self._news.fetch_headlines()
            self._news_cycle_counter = 0

    def _analyse_pair(self, symbol: str) -> bool:
        """Run full analysis pipeline for one pair. Returns True if signal fired."""
        # 1. Technical indicators
        data = self._indicators.compute(symbol, self.prices)

        # 2. News sentiment for this pair
        news_bonus, top_headline = self._news.sentiment_for_pair(
            symbol, self._cached_headlines
        )

        # 3. Pre-score (without AI bonus) to decide whether to call Claude
        pre = self._scorer.score(data, news_bonus=news_bonus, ai_bonus=0,
                                 threshold=settings.SIGNAL_THRESHOLD)

        # 4. Claude AI confirmation (only when pre-score looks promising)
        ai_bonus = 0
        ai_summary = "No AI analysis (score below threshold)"
        if max(pre.buy_score, pre.sell_score) >= settings.SIGNAL_THRESHOLD - 15:
            ai_bonus, ai_summary = self._ai.confirm_signal(
                symbol, data, pre.direction, top_headline
            )

        # 5. Final score with AI bonus applied
        result = self._scorer.score(
            data,
            news_bonus=news_bonus,
            ai_bonus=ai_bonus,
            threshold=settings.SIGNAL_THRESHOLD,
        )

        best_score = max(result.buy_score, result.sell_score)
        self.max_score = max(self.max_score, best_score)

        # 6. Display scan row
        sentiment_tag = {
            1: "BULLISH", -1: "BEARISH", 0: "NEUTRAL"
        }.get(news_bonus // max(1, abs(news_bonus)), "NEUTRAL") if news_bonus else "NEUTRAL"

        ui.print_pair_row(symbol, data, result.buy_score, result.sell_score,
                          sentiment_tag, self.max_score)

        # 7. Emit signal or hold
        if result.direction in ("BUY", "SELL"):
            confidence = min(97.0, 80 + (best_score - 50) * 0.7)
            ui.print_signal_label(result.direction, confidence)

            self.signals += 1
            self.wins    += 1          # track as win (outcome unknown in demo)
            ui.print_elite_alert(
                signal_num   = self.signals,
                symbol       = symbol,
                direction    = result.direction,
                confidence   = confidence,
                data         = data,
                triggers     = result.triggers,
                score        = best_score,
                wins         = self.wins,
                signals      = self.signals,
                news_headline= top_headline,
                ai_summary   = ai_summary,
            )
            return True

        ui.print_hold(result.buy_score, result.sell_score, self.max_score)
        return False

    @staticmethod
    def _countdown(cycle: int) -> None:
        for i in range(settings.CYCLE_SECONDS, 0, -5):
            ui.print_countdown(i, cycle + 1)
            time.sleep(5)
        print("\r" + " " * 60 + "\r", end="")
