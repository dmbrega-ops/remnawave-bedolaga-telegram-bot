"""Custom-emoji icon ids for bot buttons + text theming.

Source set: `brega_line2_by_brega_vpn_billing_bot` (title "Brega VPN line",
type=custom_emoji, 130 emoji; icons padded to ~80% of the cell so text lines
don't stick together — v1 `brega_line_…` filled ~92%), created by the bot itself via Bot API — so the bot
may use these without Telegram Premium. Monochrome Lucide line icons (ISC) in the
Ponteto green #22c55e; ❌/🚫/⛔/🛑/❗ red, ⚠️ amber. Built 2026-10-18; it replaced
the colourful `by_brega` set (kept on Telegram for rollback). The comment after
each id is the native glyph and the Lucide icon name.

- Buttons: ``icon_custom_emoji_id=BREGA_ICON['<key>']`` + ``strip_leading_emoji``.
- Message text: themed centrally by BregaEmojiMiddleware via ``emojify`` /
  ``GLYPH_TO_ID`` — do NOT hand-wrap <tg-emoji> in templates.
- Button colours: client buttons are neutral grey, only ``danger`` survives
  (see :func:`neutral_style`).
"""

import re

BREGA_ICON: dict[str, str] = {
    'connect': '5377768644841353061',  # 🔑 key-round
    'extend': '5377523269064762899',  # 🕒 clock-3
    'devices': '5380033883607704664',  # 📱 smartphone
    'privacy': '5377434779853566895',  # 🛡 shield-check
    'ticket': '5377538460364087162',  # 🎫 ticket
    'ios': '5377560038279794855',  # 🍏 apple
    'android': '5377668791146685704',  # 🤖 bot
    'macos': '5377329849507553742',  # 🖥 monitor
    'windows': '5379828382307492682',  # 💻 laptop
    'balance': '5377726730255511465',  # 💰 wallet
    'buy': '5377610431131067017',  # 💎 gem
    'traffic': '5377500299579664126',  # 📊 chart-column
    'tariff': '5377319258118202411',  # 📦 package
    'info': '5377609559252705751',  # ℹ info
    'list': '5377663877704100144',  # 📋 clipboard-list
    'link': '5377664676568018179',  # 🔗 link
    'language': '5377378528666889221',  # 🌐 globe
    'subscription': '5380033883607704664',  # 📱 smartphone
    'settings': '5377529840364727292',  # ⚙ settings
    'gift': '5377554570786418810',  # 🎁 gift
    'autopay': '5377826180223247395',  # 💳 credit-card
    'reset': '5377771840297020649',  # 🔄 refresh-cw
    'profile': '5379849084049860810',  # 👤 user
    'install': '5379875012767428097',  # 📲 download
    'back': '5377340668530172154',  # ⬅ arrow-left
    'support': '5377561339654879069',  # 🛠 wrench
    'referrals': '5379918061224633598',  # 🤝 handshake
    'rename': '5377679330996431219',  # ✏ pencil
    'unknown': '5377421950786251096',  # ❓ circle-question-mark
    'tag': '5379686094335944361',  # 🏷 tag
    'email': '5377716289190010220',  # 📧 mail
    'lock': '5380085633668655004',  # 🔒 lock
    'unlimited': '5377610456900872577',  # ♾ infinity
}


# --- Auto-replace of unicode emoji with brega_line custom emoji in MESSAGE TEXT ---
# Maps each glyph (без variation selector U+FE0F) to its custom_emoji_id. Used by
# BregaEmojiMiddleware to rewrite outgoing text/caption. NOT for button captions.
_FE0F = '️'

GLYPH_TO_ID: dict[str, str] = {
    '☰': '5379658198523356309',  # menu (not an emoji; set entry is filed under 📃)
    '📃': '5379658198523356309',  # menu
    '❌': '5377747655336176615',  # x
    '✅': '5377309152060152677',  # circle-check
    '💳': '5377826180223247395',  # credit-card
    '⚠': '5377679880752245674',  # triangle-alert
    '💰': '5377726730255511465',  # wallet
    '📱': '5380033883607704664',  # smartphone
    '📊': '5377500299579664126',  # chart-column
    '🔄': '5377771840297020649',  # refresh-cw
    'ℹ': '5377609559252705751',  # info
    '📅': '5377337159541891636',  # calendar
    '📦': '5377319258118202411',  # package
    '⬅': '5377340668530172154',  # arrow-left
    '🔙': '5377340668530172154',  # arrow-left
    '🎁': '5377554570786418810',  # gift
    '🚫': '5379648118235112360',  # ban
    '🗑': '5377389437883817854',  # trash-2
    '⏳': '5379957145427030410',  # hourglass
    '⌛': '5379957145427030410',  # hourglass
    '📋': '5377663877704100144',  # clipboard-list
    '👥': '5379983104209366395',  # users
    '🎉': '5380013143210632207',  # party-popper
    '✏': '5377679330996431219',  # pencil
    '💡': '5379581769580322446',  # lightbulb
    '🔗': '5377664676568018179',  # link
    '⏰': '5379814200325479881',  # alarm-clock
    '🌍': '5377856137620140488',  # earth
    '⚙': '5377529840364727292',  # settings
    '📈': '5379771160458206875',  # trending-up
    '💎': '5377610431131067017',  # gem
    '🌐': '5377378528666889221',  # globe
    '🎫': '5377538460364087162',  # ticket
    '🎟': '5377538460364087162',  # ticket
    '⚡': '5379823408735365568',  # zap
    '❓': '5377421950786251096',  # circle-question-mark
    '🎯': '5377460236124728403',  # target
    '👤': '5379849084049860810',  # user
    '🤝': '5379918061224633598',  # handshake
    '➕': '5380002221108801878',  # plus
    '📝': '5377608219222911518',  # notebook-pen
    '💸': '5377361396042345037',  # banknote-arrow-down
    '📄': '5377789673001232889',  # file-text
    '🧪': '5377501699739004967',  # flask-conical
    '📨': '5377673867798032179',  # mail-open
    '🚀': '5377367486305972218',  # rocket
    '🛠': '5377561339654879069',  # wrench
    '🧩': '5377401240453947694',  # puzzle
    '📌': '5377829422923558958',  # pin
    '🔒': '5380085633668655004',  # lock
    '🏦': '5380055942559736223',  # landmark
    '📡': '5377419605734105878',  # radio-tower
    '🏆': '5377299698837137356',  # trophy
    '🧑': '5377482780408061337',  # circle-user
    '⬇': '5379968763313562520',  # arrow-down
    '👇': '5379968763313562520',  # arrow-down
    '🔍': '5377359768249740750',  # search
    '🔎': '5377359768249740750',  # search
    '🪙': '5377743360368880754',  # coins
    '🏠': '5379881618427126088',  # house
    '⏭': '5377527972053952217',  # skip-forward
    '👁': '5377795415372507745',  # eye
    '🔧': '5377847801088619601',  # settings-2
    '🗓': '5377546547787510389',  # calendar-days
    '🤖': '5377668791146685704',  # bot
    '⭐': '5379947941312112490',  # star
    '⏸': '5377658010778771654',  # pause
    '🕒': '5377523269064762899',  # clock-3
    '📢': '5377739353164397693',  # megaphone
    '📣': '5377739353164397693',  # megaphone
    '⬆': '5380050041274670734',  # arrow-up
    '♻': '5379880995656868187',  # recycle
    '↩': '5379895899193384187',  # undo-2
    '⚖': '5377500948119724968',  # scale
    '🛒': '5377675151993255002',  # shopping-cart
    '❗': '5377311806349945716',  # circle-alert
    '📤': '5377622998205377546',  # upload
    '🔁': '5377814781380045218',  # repeat
    '🛟': '5377767218912211446',  # life-buoy
    '🆘': '5377767218912211446',  # life-buoy
    '⏱': '5377323252437792193',  # timer
    '🛡': '5377434779853566895',  # shield-check
    '👀': '5379619234580046514',  # scan-eye
    '🖥': '5377329849507553742',  # monitor
    '➡': '5379660294467395896',  # arrow-right
    '📆': '5377393732851116613',  # calendar-range
    '🎲': '5380094992402392855',  # dices
    '💤': '5377343816741202543',  # moon
    '🏷': '5379686094335944361',  # tag
    '📬': '5379689057863378346',  # mailbox
    '🧾': '5379790268767710109',  # receipt
    '➖': '5380040656771130785',  # minus
    '💬': '5377656090928393258',  # message-circle
    '💻': '5379828382307492682',  # laptop
    '📥': '5379875012767428097',  # download
    '📲': '5379875012767428097',  # download
    '🔐': '5377582513843646309',  # lock-keyhole
    '🗳': '5377496889375632322',  # vote
    '✖': '5377487015245816554',  # x
    '⏹': '5377472141774071273',  # square
    '🧹': '5379653113282078298',  # brush-cleaning
    '🚦': '5377854058855964384',  # traffic-cone
    '📜': '5377539400961924577',  # scroll-text
    '🚚': '5377536330060313468',  # truck
    '✉': '5377716289190010220',  # mail
    '📧': '5377716289190010220',  # mail
    '📺': '5377828924707353192',  # tv
    '🕐': '5379975201469538043',  # clock-1
    '📎': '5379925435683480520',  # paperclip
    '🔥': '5377383094217125934',  # flame
    '📷': '5377407403732020937',  # camera
    '🎥': '5377653638502068958',  # video
    '🖼': '5377689458529314761',  # image
    '🔚': '5379607075527630641',  # arrow-right-to-line
    '🏅': '5377346178973217137',  # medal
    '👋': '5377392427181057126',  # hand
    '🔔': '5380086058870420952',  # bell
    '📉': '5377453892458030229',  # trending-down
    '🗄': '5377359411767455250',  # archive
    '📶': '5377653513948014643',  # signal
    '🍎': '5377560038279794855',  # apple
    '🍏': '5377560038279794855',  # apple
    '🗂': '5377561112021609630',  # folder-open
    '⛓': '5379998497372153806',  # link-2
    '🏬': '5377471063737278265',  # store
    '💪': '5377511745667510344',  # biceps-flexed
    '📍': '5379867410675312063',  # map-pin
    '⛔': '5379825994305678728',  # circle-minus
    '🔓': '5377439839325038935',  # lock-open
    '🛑': '5379891823269422282',  # octagon-x
    '🔑': '5377768644841353061',  # key-round
    '💵': '5377822293277847031',  # banknote
    '◀': '5377854260719428350',  # chevron-left
    '👻': '5377753260268496627',  # ghost
    '🥶': '5377450697002363243',  # snowflake
    '🧊': '5377450697002363243',  # snowflake
    '♾': '5377610456900872577',  # infinity
    '🪜': '5377669452571649947',  # list-ordered
    '📰': '5377303100451236048',  # newspaper
    '🧭': '5380102474235422729',  # compass
    '🗺': '5380044745579994618',  # map
    '🔌': '5377665823324281905',  # plug
}

# Longest glyphs first so multi-codepoint emoji win over any prefix.
_GLYPH_ALT = '|'.join(re.escape(g) for g in sorted(GLYPH_TO_ID, key=len, reverse=True))
_EMOJI_RE = re.compile('(' + _GLYPH_ALT + ')(' + _FE0F + '?)')
_LEADING_GLYPH_RE = re.compile('^(' + _GLYPH_ALT + ')(' + _FE0F + '?)')
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


def split_leading_glyph(text: str | None) -> tuple[str | None, str]:
    """Если строка начинается с маппленного глифа — вернуть (emoji_id, остаток без
    ведущего глифа и одного пробела). Иначе (None, исходный текст).

    Для авто-иконок на inline-кнопках: ведущий глиф → ``icon_custom_emoji_id``,
    подпись без него. Только для глифов, реально присутствующих в наборе.
    """
    if not text:
        return None, text or ''
    match = _LEADING_GLYPH_RE.match(text)
    if not match:
        return None, text
    emoji_id = GLYPH_TO_ID.get(match.group(1))
    if not emoji_id:
        return None, text
    rest = text[match.end() :]
    if rest.startswith(' '):
        rest = rest[1:]
    return emoji_id, rest


def neutral_style(style: str | None) -> str | None:
    """House button scheme: every client button is neutral grey except ``danger``.

    Green line icons are the accent; a coloured background would repaint them
    into a white silhouette, so ``success``/``primary`` are dropped. Rich-only
    ``link`` is a shape, not a colour, so it is kept too.
    """
    return style if style in ('danger', 'link') else None


# Telegram rejects an empty button caption, so a glyph-only button (pagination
# arrows) keeps an invisible WORD JOINER next to its custom icon.
ICON_ONLY_TEXT = '\u2060'


def icon_and_caption(text: str | None) -> tuple[str | None, str]:
    """Leading mapped glyph → (emoji_id, caption); glyph-only → invisible caption."""
    emoji_id, rest = split_leading_glyph(text)
    if not emoji_id:
        return None, text or ''
    return emoji_id, rest if rest.strip() else ICON_ONLY_TEXT
