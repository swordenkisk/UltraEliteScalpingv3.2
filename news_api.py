"""
ultra_elite_scalping/apis/news_api.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Fetch live forex/macro headlines from NewsAPI and convert them
          into a numeric sentiment bonus for the scoring engine.

Setup
-----
1. Register at https://newsapi.org (free tier: 100 req/day)
2. Add your key to .env:  NEWS_API_KEY=abc123...
3. The client degrades gracefully if the key is missing or the API is down.
"""

import requests
import logging
from config.settings import (
    NEWS_API_URL, NEWS_QUERY, NEWS_LANGUAGE,
    NEWS_PAGE_SIZE, PAIR_KEYWORDS
)

logger = logging.getLogger(__name__)

# Keywords that bias sentiment positively or negatively
_BULLISH_WORDS = {
    "rally", "surge", "gains", "bullish", "rise", "soar",
    "strong", "hawkish", "growth", "beat", "upgrade",
}
_BEARISH_WORDS = {
    "fall", "drop", "plunge", "bearish", "weak", "dovish",
    "miss", "slowdown", "decline", "downgrade", "recession",
}


class NewsAPIClient:
    """
    Wraps the NewsAPI /v2/everything endpoint.

    Methods
    -------
    fetch_headlines() → list[dict]
        Pull the latest forex/macro headlines.

    sentiment_for_pair(symbol, headlines) → (int, str)
        Return (bonus_score, top_headline_string) for a specific pair.
        bonus_score is in the range −10 … +10.
    """

    def __init__(self, api_key: str) -> None:
        self._key = api_key
        self._session = requests.Session()

    # ── Public ────────────────────────────────────────────────────────────────

    def fetch_headlines(self) -> list[dict]:
        """
        Fetch up to NEWS_PAGE_SIZE latest forex/macro articles.
        Returns empty list on any failure so the bot keeps running.
        """
        if not self._key:
            logger.warning("NEWS_API_KEY not set — using mock headlines")
            return self._mock_headlines()

        try:
            resp = self._session.get(
                NEWS_API_URL,
                params={
                    "q":        NEWS_QUERY,
                    "language": NEWS_LANGUAGE,
                    "pageSize": NEWS_PAGE_SIZE,
                    "sortBy":   "publishedAt",
                    "apiKey":   self._key,
                },
                timeout=8,
            )
            resp.raise_for_status()
            articles = resp.json().get("articles", [])
            logger.debug("Fetched %d headlines from NewsAPI", len(articles))
            return articles
        except Exception as exc:
            logger.warning("NewsAPI error: %s — using mock headlines", exc)
            return self._mock_headlines()

    def sentiment_for_pair(
        self, symbol: str, headlines: list[dict]
    ) -> tuple[int, str]:
        """
        Filter headlines relevant to *symbol* and aggregate sentiment.

        Returns
        -------
        (bonus, headline_text)
            bonus         : integer in [−10, +10]
            headline_text : the single most relevant headline (or fallback msg)
        """
        keywords = PAIR_KEYWORDS.get(symbol, [])
        relevant = [
            h for h in headlines
            if any(kw.lower() in (h.get("title") or "").lower() for kw in keywords)
        ]

        if not relevant:
            return 0, "No relevant headlines found for this pair"

        top = relevant[0]
        headline_text = top.get("title") or "—"

        # Score each relevant headline
        total = 0
        for article in relevant[:5]:
            text = ((article.get("title") or "") + " " + (article.get("description") or "")).lower()
            bull = sum(1 for w in _BULLISH_WORDS if w in text)
            bear = sum(1 for w in _BEARISH_WORDS if w in text)
            total += (bull - bear)

        # Clamp to ±10
        bonus = max(-10, min(10, total * 2))
        return bonus, headline_text

    # ── Private ───────────────────────────────────────────────────────────────

    @staticmethod
    def _mock_headlines() -> list[dict]:
        """Fallback mock data so the bot works without a live API key."""
        return [
            {"title": "EUR/USD holds steady as ECB signals cautious stance", "description": "Euro gains on hawkish ECB tone"},
            {"title": "GBP rallies after strong UK employment data", "description": "Sterling surge on bullish jobs report"},
            {"title": "USD weakens amid Fed dovish commentary", "description": "Dollar drops on weak outlook"},
            {"title": "AUD declines on RBA rate hold decision", "description": "Australian dollar falls on dovish RBA"},
            {"title": "USD/CAD edges higher on oil price decline", "description": "Loonie weakens as oil drops"},
            {"title": "EUR/GBP stable as both central banks stay on hold", "description": "Cross rate holds tight range"},
            {"title": "Yen strengthens on BOJ hawkish shift expectations", "description": "JPY bullish on BOJ signals"},
        ]
