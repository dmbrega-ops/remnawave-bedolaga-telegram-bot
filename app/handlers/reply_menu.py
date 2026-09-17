"""Persistent reply-keyboard main-menu shortcuts (RU-only stand).

Adds a persistent bottom ReplyKeyboard with three shortcuts — Профиль (opens the
in-bot main menu), Подписка and Инфо — that work from ANY FSM state. Registered
before every FSM message handler, so pressing a shortcut while entering e.g. a
promocode cancels that input (state is cleared) and navigates instead of being
swallowed as the awaited text (risk #1).

The button caption and the message-text filter come from the SAME localization
call (:func:`app.keyboards.reply.nav_menu_labels`), so they can never drift.

Routing reuses the existing callback section handlers (``show_main_menu``,
``show_subscription_info``, ``show_info_menu``) through a lightweight
``CallbackQuery`` shim whose ``answer()`` is a no-op and whose ``.message`` is a
freshly sent bot message. Nothing in those prod handlers is touched, and no
section-rendering logic is duplicated.

Trade-off (v1): Профиль/Инфо go through ``edit_or_answer_photo``, which cannot
edit a plain-text placeholder into a photo, so it cleanly falls back to a text
send — i.e. those two screens open WITHOUT the logo header when reached via the
reply keyboard. Inline navigation keeps the logo as before.
"""

from aiogram import Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.config import settings
from app.database.models import User
from app.keyboards.reply import get_nav_reply_keyboard, nav_menu_labels
from app.localization.texts import get_texts


logger = structlog.get_logger(__name__)

# RU-only stand: labels/filters resolved once at registration time.
_LABELS = nav_menu_labels(settings.DEFAULT_LANGUAGE)


class _ReplyNavCallback(types.CallbackQuery):
    """A synthetic CallbackQuery used to reuse callback section handlers.

    ``answer()`` is a no-op because there is no real callback query to ack.
    ``message`` points at a freshly sent bot message the reused handler renders
    into (edit_text / edit_or_answer_photo both cope with it).
    """

    async def answer(self, *args, **kwargs):  # noqa: D401 - see class docstring
        return None


async def _open_section(message: types.Message, db_user: User, db: AsyncSession, data: str, handler) -> None:
    sent = await message.answer('⏳')
    shim = _ReplyNavCallback(
        id=f'reply_nav:{message.message_id}',
        from_user=message.from_user,
        chat_instance=str(message.chat.id),
        message=sent,
        data=data,
    )
    await handler(shim, db_user, db)


async def open_profile(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    from app.handlers.menu import show_main_menu

    await _open_section(message, db_user, db, 'menu_profile', show_main_menu)


async def open_subscription(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    from app.handlers.subscription.purchase import show_subscription_info

    await _open_section(message, db_user, db, 'menu_subscription', show_subscription_info)


async def open_info(message: types.Message, db_user: User, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
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
    dp.message.register(open_profile, F.text == _LABELS['profile'])
    dp.message.register(open_subscription, F.text == _LABELS['subscription'])
    dp.message.register(open_info, F.text == _LABELS['info'])
