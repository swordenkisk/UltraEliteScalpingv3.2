#!/usr/bin/env python3
"""
ultra_elite_scalping/main.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Application entry point.

Usage
-----
    python main.py

Environment
-----------
Copy .env.example → .env and fill in:
    ANTHROPIC_API_KEY   — Claude AI signal confirmation
    NEWS_API_KEY        — Live forex headline sentiment
    (optional) ALPHA_VANTAGE_KEY, CYCLE_SECONDS, SIGNAL_THRESHOLD
"""

import logging
import sys
import os

# Make sure project root is on sys.path when run directly
sys.path.insert(0, os.path.dirname(__file__))

from core.bot import UltraEliteBot

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bot.log", mode="a"),
    ],
)

if __name__ == "__main__":
    bot = UltraEliteBot()
    bot.run_ultra()
