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
}
