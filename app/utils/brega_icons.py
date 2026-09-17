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
}

# Still no home in the set (no matching button yet): 🗓 🌍 ✅ 🔓 ✉️ 📺 📡 🕒.
