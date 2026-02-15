"""
ultra_elite_scalping/utils/display.py
========================================
Author  : Ultra Elite Dev Team
Version : 3.2.0
Purpose : Terminal colour constants, banner, and formatted alert printing
"""

from datetime import datetime

# ── ANSI Colour Codes ─────────────────────────────────────────────────────────
GREEN    = "\033[92m"
RED      = "\033[91m"
GOLD     = "\033[93m"
PLATINUM = "\033[96m"
STEEL    = "\033[94m"
DIAMOND  = "\033[95m"
CARBON   = "\033[90m"
RESET    = "\033[0m"
BOLD     = "\033[1m"
UNDER    = "\033[4m"
FLASH    = "\033[5m"

LINE_LONG  = "=" * 95
LINE_SHORT = "-" * 95


def print_banner() -> None:
    """Print the startup banner."""
    print(f"\n{GREEN}{BOLD}{UNDER}🔥 ULTRA ELITE SCALPING v3.2 — AI + NEWS EDITION 🔥{RESET}")
    print(f"{PLATINUM}{LINE_LONG}{RESET}")
    print(f"{DIAMOND}🦁 6 PAIRS | 12 INDICATORS | AI ANALYSIS | LIVE NEWS SENTIMENT 🦁{RESET}")
    print(f"{GOLD}⚡ CYCLE: 45s | THRESHOLD: 65pts | CLAUDE AI CONFIRMATION ⚡{RESET}")
    print(f"{PLATINUM}{LINE_LONG}{RESET}\n")


def print_cycle_header(cycle: int) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n{STEEL}{BOLD}⏰ {now} | CYCLE #{cycle:03d} | ELITE SWEEP{RESET}")
    print(f"{PLATINUM}{LINE_SHORT}{RESET}")


def print_pair_row(symbol: str, data: dict, buy_score: int, sell_score: int,
                   news_sentiment: str, max_score: int) -> None:
    """Print the one-line summary row for a pair during scanning."""
    print(
        f"{PLATINUM}🔥 {symbol:<6}{RESET}"
        f"P:{data['price']:>8.5f}  RSI:{data['rsi']:>4.1f}"
        f"  S:{data['stoch']:>4.1f}  CCI:{data['cci']:>5.0f}"
        f"  News:{news_sentiment:>8s}",
        end="  "
    )


def print_hold(buy_score: int, sell_score: int, max_score: int) -> None:
    print(f"{CARBON}⏳ HOLD  {max(buy_score, sell_score):3d}/{max_score:3d}{RESET}")


def print_signal_label(direction: str, confidence: float) -> None:
    if direction == "BUY":
        print(f"{GREEN}{BOLD}{FLASH}🟢 BUY  {confidence:2.0f}% 🚀{RESET}")
    else:
        print(f"{RED}{BOLD}{FLASH}🔴 SELL {confidence:2.0f}% 💥{RESET}")


def print_elite_alert(
    signal_num: int,
    symbol: str,
    direction: str,
    confidence: float,
    data: dict,
    triggers: list[str],
    score: int,
    wins: int,
    signals: int,
    news_headline: str,
    ai_summary: str,
) -> None:
    """Full alert block printed after a confirmed signal."""
    color = GREEN if direction == "BUY" else RED
    emoji = "🟢" if direction == "BUY" else "🔴"
    pips = round(data["atr"] * 10_000 * 1.2, 1)
    sl   = round(data["atr"] * 10_000 * 0.8, 1)

    print(f"""
{color}{BOLD}{UNDER}🦁 ELITE SCALP #{signal_num} 🦁{emoji} {direction} {symbol}{RESET}{BOLD}
{LINE_LONG}
💰 ENTRY:      {data['price']:>9.5f}  |  🎯 TP: {pips:>5.1f} pips  |  🛡 SL: {sl:>5.1f} pips
📊 RSI:        {data['rsi']:>5.1f}  |  STOCH: {data['stoch']:>5.1f}  |  CCI: {data['cci']:>6.0f}
📈 EMA F/S:    {data['ema_fast']:>8.5f} / {data['ema_slow']:>8.5f}  |  MACD: {data['macd']:+8.5f}
⚡ ADX:        {data['adx']:>5.1f}  |  VOL: {data['volume']:>5.2f}x  |  ATR: {data['atr']*10000:>5.1f}
💎 SCORE:      {score:>4d}/120  |  WINRATE: {confidence:>3.0f}%  |  STATS: {wins}/{signals}
🔥 TRIGGERS:   {', '.join(triggers)}
📰 NEWS:       {news_headline[:70]}
🤖 AI TAKE:    {ai_summary[:70]}
⏰ {datetime.now().strftime('%H:%M:%S')}  |  🦁 ULTRA ELITE EXECUTION
{LINE_LONG}{RESET}
    """)


def print_cycle_footer(cycle: int, signals: int, total_signals: int,
                       total_wins: int, max_score: int) -> None:
    win_rate = (total_wins / total_signals * 100) if total_signals else 0.0
    print(f"\n{GREEN}{BOLD}✅ CYCLE #{cycle} | {signals}/{len(['EURUSD','GBPUSD','USDJPY','AUDUSD','USDCAD','EURGBP'])} SIGNALS | WR: {win_rate:5.1f}%{RESET}")
    print(f"{DIAMOND}📊 TOTAL: {total_signals} signals | MAX SCORE: {max_score}/120{RESET}")
    print(f"{GOLD}{LINE_LONG}{RESET}")


def print_countdown(seconds_left: int, next_cycle: int) -> None:
    print(f"\r{GOLD}⏳ {seconds_left:2d}s → CYCLE #{next_cycle}...{RESET}", end="", flush=True)


def print_shutdown(total_signals: int, total_wins: int) -> None:
    win_rate = (total_wins / total_signals * 100) if total_signals else 0.0
    print(f"\n{RED}{BOLD}🛑 ULTRA ELITE STOPPED{RESET}")
    print(f"{GREEN}{BOLD}📈 {total_signals} SIGNALS | {total_wins} WINS | {win_rate:5.1f}% WR{RESET}")
