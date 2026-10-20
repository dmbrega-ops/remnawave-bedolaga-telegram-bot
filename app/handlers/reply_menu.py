"""Persistent reply-keyboard main-menu shortcuts (RU-only stand).

The bottom ReplyKeyboard mirrors the inline main menu — Главная (main menu),
Подписка (subscription card, the inline «Подписка» button) and Ещё (the «☰ Ещё»
screen) — so the same section has the same name wherever it is opened. The
shortcuts work from ANY FSM state: registered before every FSM message handler,
so pressing one while entering e.g. a promocode cancels that input (state is
cleared) and navigates instead of being swallowed as the awaited text.

One menu in the chat: a shortcut deletes the previous menu the bot sent as a new
message (see :mod:`app.utils.nav_menu`) and the tapped shortcut text itself, so
stale live menus don't pile up in the chat.

The button caption and the message-text filter come from the SAME localization
call (:func:`app.keyboards.reply.nav_menu_labels`), so they can never drift.
Captions of the previous keyboard (Профиль / Инфо) are still routed and swap the
keyboard for the current one.

Подписка/Ещё reuse the existing callback section handlers through a lightweight
``CallbackQuery`` shim whose ``answer()`` is a no-op and whose ``.message`` is a
freshly sent bot message the handler edits in place.
"""

from aiogram import Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.config import settings
from app.database.models import User
from app.keyboards.reply import get_nav_reply_keyboard, legacy_nav_menu_labels, nav_menu_labels
from app.localization.texts import get_texts
from app.utils.miniapp_buttons import strip_leading_emoji
from app.utils.nav_menu import drop_previous_nav_menu, remember_nav_menu


logger = structlog.get_logger(__name__)

# RU-only stand: labels/filters resolved once at registration time.
_LABELS = nav_menu_labels(settings.DEFAULT_LANGUAGE)
_LEGACY_LABELS = legacy_nav_menu_labels(settings.DEFAULT_LANGUAGE)


def _label_variants(key: str, labels: dict[str, str] = _LABELS) -> set[str]:
    """Both the full label and the emoji-stripped one.

    The nav reply-keyboard buttons now carry a custom-emoji icon and their
    caption is stripped of the leading unicode glyph, so a tap sends the bare
    text (e.g. "Профиль"). Older cached keyboards still send the full "👤 Профиль".
    Match either so routing never drifts.
    """
    full = labels[key]
    return {full, strip_leading_emoji(full)}


class _ReplyNavCallback(types.CallbackQuery):
    """A synthetic CallbackQuery used to reuse callback section handlers.

    ``answer()`` is a no-op because there is no real callback query to ack.
    ``message`` points at a freshly sent bot message the reused handler renders
    into (edit_text / edit_or_answer_photo both cope with it).
    """

    async def answer(self, *args, **kwargs):  # noqa: D401 - see class docstring
        return None


async def _clear_chat(message: types.Message) -> None:
    """Убрать прежнее меню и нажатую подпись кнопки — в чате остаётся одно меню."""
    await drop_previous_nav_menu(message.bot, message.chat.id)
    try:
        await message.delete()
    except Exception:  # нет прав / уже удалено — не важно
        pass


async def _open_section(message: types.Message, db_user: User, db: AsyncSession, data: str, handler) -> None:
    sent = await message.answer('⏳')
    await remember_nav_menu(message.chat.id, sent.message_id)
    shim = _ReplyNavCallback(
        id=f'reply_nav:{message.message_id}',
        from_user=message.from_user,
        chat_instance=str(message.chat.id),
        message=sent,
        data=data,
    )
    await handler(shim, db_user, db)


async def open_home(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await _clear_chat(message)
    # Fresh rich message (same path as /start), not the '⏳'+edit shim: editing a
    # plain-text placeholder fell back to a reduced text menu.
    from app.handlers.menu import answer_main_menu

    await answer_main_menu(message, db_user, db)


async def open_subscription(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await _clear_chat(message)
    from app.handlers.subscription.purchase import show_subscription_info

    await _open_section(message, db_user, db, 'menu_subscription', show_subscription_info)


async def open_more(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await _clear_chat(message)
    from app.handlers.menu import show_more_menu

    await _open_section(message, db_user, db, 'menu_more', show_more_menu)


async def open_legacy_profile(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await send_main_reply_keyboard(message)
    await open_home(message, db_user, state, db)


async def open_legacy_info(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await send_main_reply_keyboard(message)
    await _clear_chat(message)
    from app.handlers.menu import show_info_menu

    await _open_section(message, db_user, db, 'menu_info', show_info_menu)


async def send_main_reply_keyboard(target_message: types.Message, language: str | None = None) -> None:
    """(Re)assert the persistent bottom reply-keyboard on a /start main menu.

    Telegram keeps a reply-keyboard until it is replaced/removed, so sending it
    on /start is enough for it to persist under subsequent inline menus. The
    caption is short and the message is silent to keep the extra message quiet.

    The keyboard is always built from ``DEFAULT_LANGUAGE`` — the same source as
    the filters registered in :func:`register_handlers` — so the button caption
    and the routing filter are guaranteed to match (RU-only stand; a per-user
    language here would silently break routing for a non-default language).
    """
    lang = settings.DEFAULT_LANGUAGE
    try:
        await target_message.answer(
            get_texts(lang).t('REPLY_MENU_HINT', '📋 Меню'),
            reply_markup=get_nav_reply_keyboard(lang),
            disable_notification=True,
        )
    except Exception as error:  # never let the keyboard break the /start flow
        logger.debug('Не удалось отправить persistent reply-клавиатуру', error=str(error))


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(open_home, F.text.in_(_label_variants('home')))
    dp.message.register(open_subscription, F.text.in_(_label_variants('subscription')))
    dp.message.register(open_more, F.text.in_(_label_variants('more')))
    dp.message.register(open_legacy_profile, F.text.in_(_label_variants('profile', _LEGACY_LABELS)))
    dp.message.register(open_legacy_info, F.text.in_(_label_variants('info', _LEGACY_LABELS)))
