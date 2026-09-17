"""Custom-emoji icon ids for bot buttons.

Source set: `brega_by` (title "Brega VPN", type=custom_emoji), created by the bot
itself — so the bot may attach these on buttons without Telegram Premium. Ids
fetched via getStickerSet 2026-09-17. The comment after each id is the set's
native fallback glyph, for eyeballing. Attach with
``icon_custom_emoji_id=BREGA_ICON['<key>']`` and strip the text's leading emoji
(``strip_leading_emoji``) so Telegram does not draw two icons.

Only concepts with a good current home are listed; the rest of the set
(🗓 🌍 ✅ 🔓 ✉️ 📺 📡) is left out until it has a button to sit on.
"""

BREGA_ICON: dict[str, str] = {
    'connect': '5285085282113202803',  # 🔑
    'extend': '5287267159859308898',   # ⏰
    'devices': '5287241845322064482',  # 📱
    'privacy': '5287721481499881198',  # 🛡
    'ticket': '5287254494000752368',   # 🎫
    'ios': '5287552805249262529',      # 🍏
    'android': '5287392061803244043',  # 🤖
    'macos': '5287395076870296095',    # 🖥
    'windows': '5287478974761446785',  # 💻
    'balance': '5287699791915034511',  # 💰
    'buy': '5287366330654172596',      # 💎
    'traffic': '5287720601031586670',  # 📈
    'tariff': '5287572330170588382',   # 📦
    'info': '5287752766041662409',     # ℹ️
    'list': '5287703605845990836',     # 📋
    'link': '5287348523719766280',     # 🔗 (a second 🔗 5287272137726403238 is spare)
    'language': '5285405252881786680',    # 🌐 → Язык + Добавить страны
    'subscription': '5287703223593903949',  # 📱 (2nd phone) → Подписка (distinct from 'devices')
    'settings': '5287363934062419345',  # ⚙️ → Настройки
    'gift': '5284993996878293721',      # 🎁 → Подарить подписку
    'autopay': '5285128506664069506',   # 💳 → Автоплатёж
    'reset': '5287676474537583251',     # 🔄 → Сбросить трафик / устройства
    'profile': '5287497919862188920',   # 👤 → Профиль
    'install': '5287734490955818181',   # 📲 → «Подключить» (rich-меню)
}

# Still no home in the set (no matching button yet): 🗓 🌍 ✅ 🔓 ✉️ 📺 📡 🕒.


# --- Auto-replace of unicode emoji with the brega_by custom emoji in MESSAGE TEXT ---
# Maps each set glyph (без variation selector U+FE0F) to its custom_emoji_id.
# Used by BregaEmojiMiddleware to rewrite outgoing text/caption. NOT applied to
# button captions (they route by text/callback — see reply-menu gotcha).
import re

_FE0F = '️'

GLYPH_TO_ID: dict[str, str] = {
    '🛡': '5287721481499881198',
    '✅': '5287408112096028678',
    '🗓': '5287458358918421962',
    '🌍': '5287299062876383249',
    '⏰': '5287267159859308898',
    '🔑': '5285085282113202803',
    '📱': '5287241845322064482',
    '🔓': '5287246200418904403',
    '🎫': '5287254494000752368',
    '✉': '5287546659151063328',
    '🍏': '5287552805249262529',
    '🤖': '5287392061803244043',
    '💻': '5287478974761446785',
    '🖥': '5287395076870296095',
    '📺': '5287499732338386038',
    '📡': '5287600599645335017',
    '💰': '5287699791915034511',
    '💎': '5287366330654172596',
    '📈': '5287720601031586670',
    '📦': '5287572330170588382',
    '🔗': '5287348523719766280',
    'ℹ': '5287752766041662409',
    '📋': '5287703605845990836',
    '🌐': '5285405252881786680',
    '🕒': '5287611053595732723',
    '⚙': '5287363934062419345',
    '🎁': '5284993996878293721',
    '💳': '5285128506664069506',
    '🔄': '5287676474537583251',
    '🏷': '5287337751941784449',
    '📲': '5287734490955818181',
    '👤': '5287497919862188920',
    '♾': '5287616705772697203',
    # Aliases: common glyph → nearest set image (fallback keeps the original glyph).
    '📅': '5287458358918421962',  # calendar → 🗓
    '📊': '5287720601031586670',  # bar chart → 📈
    '🍎': '5287552805249262529',  # red apple → 🍏
    '⏳': '5287611053595732723',  # hourglass → 🕒
}

# Longest glyphs first so multi-codepoint emoji win over any prefix.
_GLYPH_ALT = '|'.join(re.escape(g) for g in sorted(GLYPH_TO_ID, key=len, reverse=True))
# A mapped glyph + optional variation selector, captured separately.
_EMOJI_RE = re.compile('(' + _GLYPH_ALT + ')(' + _FE0F + '?)')
# Existing <tg-emoji …>…</tg-emoji> spans are left untouched (no double-wrap).
_TGEMOJI_SPAN_RE = re.compile(r'<tg-emoji\b[^>]*>.*?</tg-emoji>', re.DOTALL)


def _wrap(match: 're.Match[str]') -> str:
    glyph = match.group(1)
    return f'<tg-emoji emoji-id="{GLYPH_TO_ID[glyph]}">{glyph}{match.group(2)}</tg-emoji>'


def emojify(text: str | None) -> str | None:
    """Replace mapped unicode emoji in HTML text with brega_by <tg-emoji> tags.

    Skips text already inside <tg-emoji> spans so it is idempotent and safe over
    templates that were themed by hand. Meant for message text/caption only.
    """
    if not text or '<tg-emoji' not in text and not _EMOJI_RE.search(text):
        return text
    out: list[str] = []
    last = 0
    for span in _TGEMOJI_SPAN_RE.finditer(text):
        out.append(_EMOJI_RE.sub(_wrap, text[last:span.start()]))
        out.append(span.group(0))
        last = span.end()
    out.append(_EMOJI_RE.sub(_wrap, text[last:]))
    return ''.join(out)
