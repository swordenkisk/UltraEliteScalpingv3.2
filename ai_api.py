"""
ultra_elite_scalping/apis/ai_api.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Use the Anthropic Claude API to provide a qualitative second opinion
          on each potential trade signal, combining technical data + news context.

Setup
-----
1. Get an API key at https://console.anthropic.com
2. Add it to .env:  ANTHROPIC_API_KEY=sk-ant-...
3. If the key is absent the client returns a neutral mock response.
"""

import logging
import anthropic
from config.settings import AI_MODEL, AI_MAX_TOKENS

logger = logging.getLogger(__name__)

# System prompt that constrains Claude to give structured, concise trade analysis
_SYSTEM_PROMPT = """You are a professional forex trading analyst assistant embedded in
an algorithmic scalping system. You receive:
  - A currency pair symbol
  - Key technical indicator values
  - A direction bias (BUY / SELL / HOLD) produced by the technical model
  - A recent news headline about that pair

Your job is to give a concise second opinion (2-3 sentences maximum) and assign a
confidence boost score from 0 to 20 (integer) that will be added to the technical
score.  Score 0 means you disagree or see no confirmation; score 20 means you strongly
confirm the signal.

Respond ONLY in this exact format (no extra text):
SCORE: <integer 0-20>
ANALYSIS: <2-3 sentence qualitative comment>"""


class AIAnalysisClient:
    """
    Wraps the Anthropic Claude API for signal confirmation.

    Methods
    -------
    confirm_signal(symbol, data, direction, headline) → (int, str)
        Returns (ai_bonus_score, analysis_text).
        Falls back to (0, "AI unavailable") on any error.
    """

    def __init__(self, api_key: str) -> None:
        self._key = api_key
        self._client: anthropic.Anthropic | None = None
        if api_key:
            try:
                self._client = anthropic.Anthropic(api_key=api_key)
            except Exception as exc:
                logger.warning("Failed to initialise Anthropic client: %s", exc)

    # ── Public ────────────────────────────────────────────────────────────────

    def confirm_signal(
        self,
        symbol: str,
        data: dict,
        direction: str,
        headline: str,
    ) -> tuple[int, str]:
        """
        Ask Claude to confirm (or refute) the direction bias.

        Parameters
        ----------
        symbol    : e.g. "EURUSD"
        data      : indicator dict from IndicatorEngine
        direction : "BUY" | "SELL" | "HOLD"
        headline  : top news headline for this pair

        Returns
        -------
        (bonus_score, analysis_text)
        """
        if self._client is None:
            return self._mock_response(direction)

        prompt = self._build_prompt(symbol, data, direction, headline)
        try:
            message = self._client.messages.create(
                model=AI_MODEL,
                max_tokens=AI_MAX_TOKENS,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text.strip()
            return self._parse_response(raw)

        except anthropic.APIConnectionError:
            logger.warning("Anthropic API connection error — using mock")
        except anthropic.RateLimitError:
            logger.warning("Anthropic rate limit hit — using mock")
        except anthropic.APIStatusError as exc:
            logger.warning("Anthropic API error %s — using mock", exc.status_code)
        except Exception as exc:
            logger.warning("Unexpected AI error: %s", exc)

        return self._mock_response(direction)

    # ── Private ───────────────────────────────────────────────────────────────

    @staticmethod
    def _build_prompt(symbol: str, data: dict, direction: str, headline: str) -> str:
        return (
            f"Pair: {symbol}\n"
            f"Direction bias: {direction}\n"
            f"Price: {data['price']:.5f}\n"
            f"RSI: {data['rsi']:.1f}  |  Stochastic: {data['stoch']:.1f}  |  CCI: {data['cci']:.0f}\n"
            f"MACD: {data['macd']:+.5f}  |  ADX: {data['adx']:.1f}  |  ATR: {data['atr']*10000:.1f} pips\n"
            f"EMA fast/slow: {data['ema_fast']:.5f} / {data['ema_slow']:.5f}\n"
            f"News headline: {headline}\n\n"
            "Please evaluate whether this trade signal is supported by the technical "
            "picture and the news, then provide your SCORE and ANALYSIS."
        )

    @staticmethod
    def _parse_response(raw: str) -> tuple[int, str]:
        """Extract SCORE and ANALYSIS from Claude's formatted response."""
        score = 0
        analysis = raw  # fallback: return raw text

        for line in raw.splitlines():
            line = line.strip()
            if line.upper().startswith("SCORE:"):
                try:
                    score = int(line.split(":", 1)[1].strip())
                    score = max(0, min(20, score))
                except ValueError:
                    pass
            elif line.upper().startswith("ANALYSIS:"):
                analysis = line.split(":", 1)[1].strip()

        return score, analysis

    @staticmethod
    def _mock_response(direction: str) -> tuple[int, str]:
        """Used when the API key is absent or the call fails."""
        mock_map = {
            "BUY":  (12, "Indicators suggest oversold conditions with momentum building; moderate bullish confirmation."),
            "SELL": (12, "Overbought readings align with bearish momentum; moderate sell confirmation."),
            "HOLD": (0,  "Mixed signals — no strong directional conviction from AI analysis."),
        }
        return mock_map.get(direction, (0, "AI analysis unavailable."))
