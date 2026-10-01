"""Rewrite outgoing message text/caption to use brega_by custom emoji.

A single session-level request middleware replaces mapped unicode emoji with
``<tg-emoji>`` tags (see :func:`app.utils.brega_icons.emojify`) on every send/
edit call, so the whole bot's message TEXT is themed without touching each
template. Text/caption theming applies only when the effective parse mode is
HTML and the call carries no manual entities (custom-emoji tags need HTML
parsing).

It also auto-wires custom-emoji icons on INLINE-keyboard buttons whose caption
starts with a mapped glyph (see :func:`_theme_inline_buttons`): inline buttons
route by ``callback_data``, so rewriting their text is safe. REPLY keyboards are
left untouched — they route by button TEXT (см. reply-menu), so stripping their
captions would break routing. Admin buttons (callback_data starting with
``admin``) are skipped.
"""

from __future__ import annotations

from typing import Any

from aiogram import Bot
from aiogram.client.default import Default
from aiogram.client.session.middlewares.base import BaseRequestMiddleware, NextRequestMiddlewareType
from aiogram.enums import ParseMode
from aiogram.methods import TelegramMethod

from app.utils.brega_icons import emojify, split_leading_glyph


def _effective_parse_mode(method: TelegramMethod[Any], bot: Bot) -> Any:
    pm = getattr(method, 'parse_mode', None)
    if isinstance(pm, Default):
        return bot.default.parse_mode if bot.default else None
    return pm


def _is_html(pm: Any) -> bool:
    if pm is None:
        return False
    # ParseMode is a (str, Enum); str(ParseMode.HTML) is "ParseMode.HTML", so
    # compare the .value ("HTML"). Plain strings pass through unchanged.
    value = getattr(pm, 'value', pm)
    return str(value).upper() == ParseMode.HTML.value.upper()


def _theme_inline_buttons(reply_markup: Any) -> None:
    """Авто-иконки для inline-кнопок: подпись начинается с глифа из набора →
    проставляем ``icon_custom_emoji_id`` и срезаем ведущий глиф.

    Только ``inline_keyboard`` (маршрутизируется по callback_data — менять текст
    безопасно, в отличие от reply-клавиатур, что роутятся по тексту). Пропускаем:
    reply-клавиатуры, кнопки с уже проставленной иконкой, админские кнопки
    (callback_data начинается с ``admin``) и кнопки-«только глиф» (пустая подпись
    недопустима в Telegram).
    """
    rows = getattr(reply_markup, 'inline_keyboard', None)
    if not rows:
        return
    for row in rows:
        for button in row:
            if getattr(button, 'icon_custom_emoji_id', None):
                continue
            if (getattr(button, 'callback_data', None) or '').startswith('admin'):
                continue
            emoji_id, rest = split_leading_glyph(getattr(button, 'text', None))
            if emoji_id and rest.strip():
                button.icon_custom_emoji_id = emoji_id
                button.text = rest


class BregaEmojiMiddleware(BaseRequestMiddleware):
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[Any],
        bot: Bot,
        method: TelegramMethod[Any],
    ) -> Any:
        try:
            # Инлайн-кнопки — независимо от parse_mode (иконки не парсятся как HTML).
            _theme_inline_buttons(getattr(method, 'reply_markup', None))
            if _is_html(_effective_parse_mode(method, bot)):
                # Text (SendMessage, EditMessageText, …) — only when no manual entities.
                if getattr(method, 'text', None) and not getattr(method, 'entities', None):
                    new = emojify(method.text)
                    if new != method.text:
                        method.text = new
                # Caption (SendPhoto, EditMessageCaption, …) — only without caption_entities.
                if getattr(method, 'caption', None) and not getattr(method, 'caption_entities', None):
                    new = emojify(method.caption)
                    if new != method.caption:
                        method.caption = new
        except Exception:  # never let theming break an outgoing request
            pass
        return await make_request(bot, method)
