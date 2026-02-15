# 🦁 Ultra Elite Scalping v3.2

> **AI-powered forex scalping signal bot** — 6 pairs · 12 indicators · Live news sentiment · Claude AI confirmation

---

## ✨ What's New in v3.2

| Feature | v3.1 | v3.2 |
|---|---|---|
| Currency pairs | 3 | **6** |
| Indicators | 10 | **12** (+ Bollinger Bands, Momentum) |
| News sentiment | ❌ | ✅ **NewsAPI integration** |
| AI confirmation | ❌ | ✅ **Claude AI (Anthropic)** |
| Repository structure | Single file | **Modular package** |

### New Currency Pairs
- `AUDUSD` — Australian Dollar / US Dollar  
- `USDCAD` — US Dollar / Canadian Dollar  
- `EURGBP` — Euro / British Pound  

---

## 📁 Repository Structure

```
ultra_elite_scalping/
├── main.py                  ← Entry point (run this)
├── requirements.txt
├── .env.example             ← Copy to .env and add your API keys
│
├── config/
│   ├── __init__.py
│   └── settings.py          ← All configuration (pairs, thresholds, API URLs)
│
├── core/
│   ├── __init__.py
│   ├── bot.py               ← Main orchestrator (UltraEliteBot)
│   ├── indicators.py        ← 12-indicator engine (IndicatorEngine)
│   └── scoring.py           ← Signal scoring with news + AI bonuses (ScoringEngine)
│
├── apis/
│   ├── __init__.py
│   ├── news_api.py          ← NewsAPI client + sentiment parser
│   └── ai_api.py            ← Anthropic Claude API client
│
├── utils/
│   ├── __init__.py
│   └── display.py           ← All terminal colours & formatted output
│
└── logs/
    └── bot.log              ← Auto-generated runtime log
```

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/swordenkisk/ultra_elite_scalping.git
cd ultra_elite_scalping
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your keys:
```

| Key | Where to get it | Required? |
|---|---|---|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com | Recommended |
| `NEWS_API_KEY` | https://newsapi.org (free tier) | Recommended |
| `ALPHA_VANTAGE_KEY` | https://alphavantage.co | Optional (live prices) |

### 3. Run
```bash
python main.py
```

---

## ⚙️ Configuration

All settings live in `config/settings.py` and can be overridden via `.env`:

```python
CYCLE_SECONDS    = 45    # seconds between sweeps
SIGNAL_THRESHOLD = 65    # minimum score to fire a signal
NEWS_REFRESH_CYCLES = 3  # refresh news every N cycles
```

### Score Weights (total = 120 pts)

| Component | Points |
|---|---|
| Price Action (EMA crossover) | 25 |
| RSI Extremes | 20 |
| Stochastic | 18 |
| MACD | 15 |
| ADX Trend Strength | 12 |
| News Sentiment Bonus | ±10 |
| Claude AI Confirmation | 0–20 |

---

## 🤖 AI Analysis Pipeline

For each pair, when the pre-score is within 15 points of the threshold:

1. **NewsAPIClient** fetches the latest forex/macro headlines
2. **Sentiment scorer** checks headlines for bullish/bearish keywords and returns a ±10 bonus
3. **AIAnalysisClient** sends indicator data + top headline to Claude Sonnet, which returns:
   - An integer score 0–20 (confidence boost)
   - A 2-3 sentence qualitative analysis
4. Final score = technical score + news bonus + AI bonus

If no API keys are configured the bot **degrades gracefully**: mock headlines and mock AI responses are used, so it always runs.

---

## 📰 News Sentiment

Headlines are fetched from [NewsAPI](https://newsapi.org) with keywords:
```
forex OR currency OR EUR OR USD OR GBP OR JPY OR AUD OR CAD
```

Pair-specific filtering uses `PAIR_KEYWORDS` in `config/settings.py` — e.g., `AUDUSD` matches articles mentioning "AUD", "Australian dollar", "RBA", etc.

---

## ⚠️ Disclaimer

This software is for **educational and research purposes only**.  
It does **not** constitute financial advice.  
Always test in a paper-trading environment before risking real capital.  
Past signal performance does not guarantee future results.

---

## 👥 Authors

**Ultra Elite Dev Team**  
Version 3.2.0 — February 2026  

Built on:
- [Anthropic Claude](https://anthropic.com) — AI signal confirmation  
- [NewsAPI](https://newsapi.org) — Live market headlines  
- [colorama](https://github.com/tartley/colorama) — Terminal colours  
- [python-dotenv](https://github.com/theskumar/python-dotenv) — Environment config  

---

## 📄 License

MIT — see `LICENSE` for details.
