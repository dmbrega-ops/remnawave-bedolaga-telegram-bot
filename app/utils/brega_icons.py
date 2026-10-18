"""Custom-emoji icon ids for bot buttons + text theming.

Source set: `brega_line_by_brega_vpn_billing_bot` (title "Brega VPN line",
type=custom_emoji, 129 emoji), created by the bot itself via Bot API — so the bot
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
    'connect': '5377770504562191368',  # 🔑 key-round
    'extend': '5379574854682977560',  # 🕒 clock-3
    'devices': '5377608081783957640',  # 📱 smartphone
    'privacy': '5380071228348343945',  # 🛡 shield-check
    'ticket': '5377330837350037166',  # 🎫 ticket
    'ios': '5380049263885589852',  # 🍏 apple
    'android': '5380061375693366672',  # 🤖 bot
    'macos': '5377805963812184320',  # 🖥 monitor
    'windows': '5379620845192782713',  # 💻 laptop
    'balance': '5377585125183758983',  # 💰 wallet
    'buy': '5377778613460443376',  # 💎 gem
    'traffic': '5379785952325575104',  # 📊 chart-column
    'tariff': '5377497417656605187',  # 📦 package
    'info': '5377703030625968975',  # ℹ info
    'list': '5377656370101265645',  # 📋 clipboard-list
    'link': '5377400295561143869',  # 🔗 link
    'language': '5379712637233831621',  # 🌐 globe
    'subscription': '5377608081783957640',  # 📱 smartphone
    'settings': '5377730295078366773',  # ⚙ settings
    'gift': '5377782040844347851',  # 🎁 gift
    'autopay': '5377623509306483812',  # 💳 credit-card
    'reset': '5377319721974668892',  # 🔄 refresh-cw
    'profile': '5379823249821573695',  # 👤 user
    'install': '5379592532768366866',  # 📲 download
    'back': '5377685189331819751',  # ⬅ arrow-left
    'support': '5377343245510561435',  # 🛠 wrench
    'referrals': '5377606063149330225',  # 🤝 handshake
    'rename': '5377829878190092004',  # ✏ pencil
    'unknown': '5377796059617602935',  # ❓ circle-question-mark
    'tag': '5377813905206715943',  # 🏷 tag
    'email': '5377684892979077013',  # 📧 mail
    'lock': '5377749107035122738',  # 🔒 lock
    'unlimited': '5379695788077134120',  # ♾ infinity
}


# --- Auto-replace of unicode emoji with brega_line custom emoji in MESSAGE TEXT ---
# Maps each glyph (без variation selector U+FE0F) to its custom_emoji_id. Used by
# BregaEmojiMiddleware to rewrite outgoing text/caption. NOT for button captions.
_FE0F = '️'

GLYPH_TO_ID: dict[str, str] = {
    '☰': '5379993910347081404',  # menu (not an emoji; set entry is filed under 📃)
    '📃': '5379993910347081404',  # menu
    '❌': '5377302645184703818',  # x
    '✅': '5377379963185964956',  # circle-check
    '💳': '5377623509306483812',  # credit-card
    '⚠': '5377559840711289080',  # triangle-alert
    '💰': '5377585125183758983',  # wallet
    '📱': '5377608081783957640',  # smartphone
    '📊': '5379785952325575104',  # chart-column
    '🔄': '5377319721974668892',  # refresh-cw
    'ℹ': '5377703030625968975',  # info
    '📅': '5379852661757617007',  # calendar
    '📦': '5377497417656605187',  # package
    '⬅': '5377685189331819751',  # arrow-left
    '🔙': '5377685189331819751',  # arrow-left
    '🎁': '5377782040844347851',  # gift
    '🚫': '5379923777826106450',  # ban
    '🗑': '5379817473090561630',  # trash-2
    '⏳': '5377532357215563447',  # hourglass
    '⌛': '5377532357215563447',  # hourglass
    '📋': '5377656370101265645',  # clipboard-list
    '👥': '5377600131799490550',  # users
    '🎉': '5377629170073381403',  # party-popper
    '✏': '5377829878190092004',  # pencil
    '💡': '5379752868192494517',  # lightbulb
    '🔗': '5377400295561143869',  # link
    '⏰': '5377322612487659420',  # alarm-clock
    '🌍': '5377487925778885500',  # earth
    '⚙': '5377730295078366773',  # settings
    '📈': '5379992553137414798',  # trending-up
    '💎': '5377778613460443376',  # gem
    '🌐': '5379712637233831621',  # globe
    '🎫': '5377330837350037166',  # ticket
    '🎟': '5377330837350037166',  # ticket
    '⚡': '5377453475846209391',  # zap
    '❓': '5377796059617602935',  # circle-question-mark
    '🎯': '5377376982478663459',  # target
    '👤': '5379823249821573695',  # user
    '🤝': '5377606063149330225',  # handshake
    '➕': '5379941765149138958',  # plus
    '📝': '5379821205417141950',  # notebook-pen
    '💸': '5377714438059110563',  # banknote-arrow-down
    '📄': '5377345380109294323',  # file-text
    '🧪': '5377309796305252656',  # flask-conical
    '📨': '5377784046594073932',  # mail-open
    '🚀': '5377526245477098012',  # rocket
    '🛠': '5377343245510561435',  # wrench
    '🧩': '5377410470338672118',  # puzzle
    '📌': '5379752412925961731',  # pin
    '🔒': '5377749107035122738',  # lock
    '🏦': '5377565385514066827',  # landmark
    '📡': '5379795607412058681',  # radio-tower
    '🏆': '5377541174783418766',  # trophy
    '🧑': '5377407163213847992',  # circle-user
    '⬇': '5377591215447383471',  # arrow-down
    '👇': '5377591215447383471',  # arrow-down
    '🔍': '5379781206386713718',  # search
    '🔎': '5379781206386713718',  # search
    '🪙': '5377825312639853442',  # coins
    '🏠': '5377432563650441713',  # house
    '⏭': '5377437769150804764',  # skip-forward
    '👁': '5379903488400598807',  # eye
    '🔧': '5377721417380962579',  # settings-2
    '🗓': '5377370810610656879',  # calendar-days
    '🤖': '5380061375693366672',  # bot
    '⭐': '5377785545537660611',  # star
    '⏸': '5379730856485104189',  # pause
    '🕒': '5379574854682977560',  # clock-3
    '📢': '5379852395469646422',  # megaphone
    '📣': '5379852395469646422',  # megaphone
    '⬆': '5377600552706288369',  # arrow-up
    '♻': '5377714833196098985',  # recycle
    '↩': '5377527941989183881',  # undo-2
    '⚖': '5379986690507057096',  # scale
    '🛒': '5377784196917933604',  # shopping-cart
    '❗': '5377342691459770661',  # circle-alert
    '📤': '5377754784981890312',  # upload
    '🔁': '5379618461485934387',  # repeat
    '🛟': '5377564689729365607',  # life-buoy
    '🆘': '5377564689729365607',  # life-buoy
    '⏱': '5377475427424053720',  # timer
    '🛡': '5380071228348343945',  # shield-check
    '👀': '5379897415316840448',  # scan-eye
    '🖥': '5377805963812184320',  # monitor
    '➡': '5379803029115544157',  # arrow-right
    '📆': '5379775154777796547',  # calendar-range
    '🎲': '5379761333573035462',  # dices
    '💤': '5377696334771957816',  # moon
    '🏷': '5377813905206715943',  # tag
    '📬': '5377455734999000145',  # mailbox
    '🧾': '5377537498291416638',  # receipt
    '➖': '5379987240262868841',  # minus
    '💬': '5377696759973719363',  # message-circle
    '💻': '5379620845192782713',  # laptop
    '📥': '5379592532768366866',  # download
    '📲': '5379592532768366866',  # download
    '🔐': '5379895585660778443',  # lock-keyhole
    '🗳': '5377727563479167883',  # vote
    '✖': '5377579150884252921',  # x
    '⏹': '5377498852175684243',  # square
    '🧹': '5377457796583303766',  # brush-cleaning
    '🚦': '5379554324739305545',  # traffic-cone
    '📜': '5379992523072643825',  # scroll-text
    '🚚': '5377754458564370488',  # truck
    '✉': '5377684892979077013',  # mail
    '📧': '5377684892979077013',  # mail
    '📺': '5377426430437141938',  # tv
    '🕐': '5377768756510502433',  # clock-1
    '📎': '5377712672827547164',  # paperclip
    '🔥': '5379677229523445582',  # flame
    '📷': '5379808569623358170',  # camera
    '🎥': '5377472141774071248',  # video
    '🖼': '5377818814354334680',  # image
    '🔚': '5377406171076404600',  # arrow-right-to-line
    '🏅': '5380041597368968784',  # medal
    '👋': '5377386848018538471',  # hand
    '🔔': '5377497078354191505',  # bell
    '📉': '5377603786816663548',  # trending-down
    '🗄': '5379700692929782407',  # archive
    '📶': '5377335372835501496',  # signal
    '🍎': '5380049263885589852',  # apple
    '🍏': '5380049263885589852',  # apple
    '🗂': '5379846661688304185',  # folder-open
    '⛓': '5377701832330092804',  # link-2
    '🏬': '5380104007538745970',  # store
    '💪': '5379625582541709860',  # biceps-flexed
    '📍': '5377358595723666703',  # map-pin
    '⛔': '5379923502948195546',  # circle-minus
    '🔓': '5377687263801026930',  # lock-open
    '🛑': '5377833262624320132',  # octagon-x
    '🔑': '5377770504562191368',  # key-round
    '💵': '5377687594513509757',  # banknote
    '◀': '5379732613126726740',  # chevron-left
    '👻': '5377761425001326159',  # ghost
    '🥶': '5377479018016711932',  # snowflake
    '🧊': '5377479018016711932',  # snowflake
    '♾': '5379695788077134120',  # infinity
    '🪜': '5380025967982978623',  # list-ordered
    '📰': '5377422401757814915',  # newspaper
    '🧭': '5377712672827547165',  # compass
    '🗺': '5380019276423931554',  # map
    '🔌': '5379596565742656730',  # plug
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
