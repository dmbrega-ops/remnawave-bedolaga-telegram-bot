"""Rewrite outgoing message text/caption to use brega_by custom emoji.

A single session-level request middleware replaces mapped unicode emoji with
``<tg-emoji>`` tags (see :func:`app.utils.brega_icons.emojify`) on every send/
edit call, so the whole bot's message TEXT is themed without touching each
template. It deliberately does NOT touch ``reply_markup`` button captions —
those route by text/callback and stripping/altering them breaks routing
(см. reply-menu). Applied only when the effective parse mode is HTML and the
call carries no manual entities (custom-emoji tags need HTML parsing).
"""

from __future__ import annotations

from typing import Any

from aiogram import Bot
from aiogram.client.default import Default
from aiogram.client.session.middlewares.base import BaseRequestMiddleware, NextRequestMiddlewareType
from aiogram.enums import ParseMode
from aiogram.methods import TelegramMethod

from app.utils.brega_icons import emojify


def _effective_parse_mode(method: TelegramMethod[Any], bot: Bot) -> Any:
    pm = getattr(method, 'parse_mode', None)
    if isinstance(pm, Default):
        return bot.default.parse_mode if bot.default else None
    return pm


def _is_html(pm: Any) -> bool:
    return pm is not None and str(pm).upper() == ParseMode.HTML.value.upper()


class BregaEmojiMiddleware(BaseRequestMiddleware):
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[Any],
        bot: Bot,
        method: TelegramMethod[Any],
    ) -> Any:
        try:
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
