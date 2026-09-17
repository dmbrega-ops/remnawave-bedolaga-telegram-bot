"""Custom-emoji icon ids for bot buttons + text theming.

Source set: `by_brega` (title "Brega VPN", type=custom_emoji, 36 emoji), created
by the bot itself — so the bot may use these without Telegram Premium. Ids
fetched via getStickerSet 2026-09-17 (full set refresh; the old `brega_by` set
was replaced, all ids changed). The comment after each id is the native glyph.

- Buttons: ``icon_custom_emoji_id=BREGA_ICON['<key>']`` + ``strip_leading_emoji``.
- Message text: themed centrally by BregaEmojiMiddleware via ``emojify`` /
  ``GLYPH_TO_ID`` — do NOT hand-wrap <tg-emoji> in templates.
"""

import re

BREGA_ICON: dict[str, str] = {
    'connect': '5287352028413079835',   # 🔑
    'extend': '5287566016568669965',    # 🕒 (set has no ⏰; clock = "time left/extend")
    'devices': '5287284773520191914',   # 📱
    'privacy': '5287411908847121699',   # 🛡
    'ticket': '5289546627852314721',    # 🎫
    'ios': '5287272391129478266',       # 🍏
    'android': '5287743484617340136',   # 🤖
    'macos': '5287716954604351965',     # 🖥
    'windows': '5287570178391977273',   # 💻
    'balance': '5287742870437013079',   # 💰
    'buy': '5287733812350985564',       # 💎
    'traffic': '5287530626038146718',   # 📊 (set has no 📈; chart)
    'tariff': '5287291739957145701',    # 📦
    'info': '5287256332246761137',      # ℹ️
    'list': '5287242300588599215',      # 📋
    'link': '5287719638958909492',      # 🔗
    'language': '5287753367337082025',  # 🌐
    'subscription': '5287284773520191914',  # 📱 (single phone in this set → same as devices)
    'settings': '5287437468197497073',  # ⚙️
    'gift': '5287601677682123015',      # 🎁
    'autopay': '5287285928866392056',   # 💳
    'reset': '5287741143860160953',     # 🔄
    'profile': '5287489261208119096',   # 👤
    'install': '5287282626036544364',   # 📲
    # New glyphs available in this set (wire onto their buttons when useful):
    'back': '5287716190100171381',      # ⬅️ → Назад
    'support': '5287288278213502348',   # 🛠 → Техподдержка
    'referrals': '5287266086117485763', # 🤝 → Партнёрка
    'rename': '5287250010054895565',    # ✏️ → переименовать устройство
    'unknown': '5287588066930765010',   # ❓
    'tag': '5287684033680028976',       # 🏷️
    'email': '5287677913351629571',     # 📧
    'lock': '5287364170285626919',      # 🔒
    'unlimited': '5287521640966565836', # ♾️
}


# --- Auto-replace of unicode emoji with by_brega custom emoji in MESSAGE TEXT ---
# Maps each glyph (без variation selector U+FE0F) to its custom_emoji_id. Used by
# BregaEmojiMiddleware to rewrite outgoing text/caption. NOT for button captions.
_FE0F = '️'

GLYPH_TO_ID: dict[str, str] = {
    '❓': '5287588066930765010',
    '⬅': '5287716190100171381',
    '🛠': '5287288278213502348',
    '🤝': '5287266086117485763',
    '✏': '5287250010054895565',
    '📲': '5287282626036544364',
    '🏷': '5287684033680028976',
    '🔄': '5287741143860160953',
    '💳': '5287285928866392056',
    '🎁': '5287601677682123015',
    '⚙': '5287437468197497073',
    '👤': '5287489261208119096',
    '📋': '5287242300588599215',
    '🔗': '5287719638958909492',
    'ℹ': '5287256332246761137',
    '♾': '5287521640966565836',
    '📦': '5287291739957145701',
    '📊': '5287530626038146718',
    '💎': '5287733812350985564',
    '💰': '5287742870437013079',
    '📡': '5287256761743485163',
    '📺': '5287367284136913974',
    '🖥': '5287716954604351965',
    '💻': '5287570178391977273',
    '🤖': '5287743484617340136',
    '🍏': '5287272391129478266',
    '📧': '5287677913351629571',
    '🎫': '5289546627852314721',
    '🔒': '5287364170285626919',
    '📱': '5287284773520191914',
    '🔑': '5287352028413079835',
    '🕒': '5287566016568669965',
    '🌐': '5287753367337082025',
    '📅': '5287275672484490360',
    '✅': '5287463749102382131',
    '🛡': '5287411908847121699',
    # Aliases: glyph seen in text → nearest set image (fallback keeps original glyph).
    '🗓': '5287275672484490360',  # spiral calendar → 📅
    '📈': '5287530626038146718',  # chart up → 📊
    '🍎': '5287272391129478266',  # red apple → 🍏
    '⏳': '5287566016568669965',  # hourglass → 🕒
    '⏰': '5287566016568669965',  # alarm → 🕒
    '✉': '5287677913351629571',  # envelope → 📧
    '🌍': '5287753367337082025',  # globe EU → 🌐
    '🔓': '5287364170285626919',  # open lock → 🔒
}

# Longest glyphs first so multi-codepoint emoji win over any prefix.
_GLYPH_ALT = '|'.join(re.escape(g) for g in sorted(GLYPH_TO_ID, key=len, reverse=True))
_EMOJI_RE = re.compile('(' + _GLYPH_ALT + ')(' + _FE0F + '?)')
_TGEMOJI_SPAN_RE = re.compile(r'<tg-emoji\b[^>]*>.*?</tg-emoji>', re.DOTALL)


def _wrap(match: 're.Match[str]') -> str:
    glyph = match.group(1)
    return f'<tg-emoji emoji-id="{GLYPH_TO_ID[glyph]}">{glyph}{match.group(2)}</tg-emoji>'


def emojify(text: str | None) -> str | None:
    """Replace mapped unicode emoji in HTML text with by_brega <tg-emoji> tags.

    Skips text already inside <tg-emoji> spans so it is idempotent. Message
    text/caption only.
    """
    if not text or ('<tg-emoji' not in text and not _EMOJI_RE.search(text)):
        return text
    out: list[str] = []
    last = 0
    for span in _TGEMOJI_SPAN_RE.finditer(text):
        out.append(_EMOJI_RE.sub(_wrap, text[last:span.start()]))
        out.append(span.group(0))
        last = span.end()
    out.append(_EMOJI_RE.sub(_wrap, text[last:]))
    return ''.join(out)
