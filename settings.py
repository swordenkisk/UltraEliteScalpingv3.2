"""
ultra_elite_scalping/config/settings.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Centralised configuration — currency pairs, thresholds, API endpoints
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ── API Keys ──────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
ALPHA_VANTAGE_KEY: str = os.getenv("ALPHA_VANTAGE_KEY", "")

# ── Currency Pairs (original 3 + 3 new) ───────────────────────────────────────
PAIRS: dict[str, float] = {
    # Original pairs
    "EURUSD": 1.0850,
    "GBPUSD": 1.2750,
    "USDJPY": 149.50,
    # New pairs
    "AUDUSD": 0.6520,
    "USDCAD": 1.3680,
    "EURGBP": 0.8510,
}

# News keywords mapped to pairs for relevance filtering
PAIR_KEYWORDS: dict[str, list[str]] = {
    "EURUSD": ["EUR", "euro", "ECB", "eurozone", "USD", "Federal Reserve", "Fed"],
    "GBPUSD": ["GBP", "pound", "sterling", "BOE", "Bank of England", "USD"],
    "USDJPY": ["JPY", "yen", "BOJ", "Bank of Japan", "USD"],
    "AUDUSD": ["AUD", "Australian dollar", "RBA", "Reserve Bank Australia", "USD"],
    "USDCAD": ["CAD", "Canadian dollar", "BOC", "Bank of Canada", "oil", "USD"],
    "EURGBP": ["EUR", "euro", "ECB", "GBP", "pound", "sterling"],
}

# ── Scoring & Signal Settings ─────────────────────────────────────────────────
SIGNAL_THRESHOLD: int = int(os.getenv("SIGNAL_THRESHOLD", 65))
MAX_SCORE: int = 120

# Score weights per indicator (must sum to MAX_SCORE)
SCORE_WEIGHTS: dict[str, int] = {
    "price_action": 25,
    "rsi":          20,
    "stoch_cci":    18,
    "macd":         15,
    "adx":          12,
    "news_boost":   10,   # AI-assisted news sentiment bonus (new)
    "ai_confirm":   20,   # Claude AI confirmation bonus (new)
}

# ── Cycle Settings ────────────────────────────────────────────────────────────
CYCLE_SECONDS: int = int(os.getenv("CYCLE_SECONDS", 45))
PAIR_DELAY: float = 0.6          # seconds between pair scans
NEWS_REFRESH_CYCLES: int = 3     # refresh news every N cycles

# ── News API ──────────────────────────────────────────────────────────────────
NEWS_API_URL: str = "https://newsapi.org/v2/everything"
NEWS_QUERY: str = "forex OR currency OR EUR OR USD OR GBP OR JPY OR AUD OR CAD"
NEWS_LANGUAGE: str = "en"
NEWS_PAGE_SIZE: int = 10

# ── Claude AI ─────────────────────────────────────────────────────────────────
AI_MODEL: str = "claude-sonnet-4-5-20250929"
AI_MAX_TOKENS: int = 400
AI_TEMPERATURE: float = 0.2     # low temperature = deterministic analysis
