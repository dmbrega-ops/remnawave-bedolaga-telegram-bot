"""Одно меню в чате: нижние кнопки убирают предыдущее меню, прежде чем показать новое.

Кнопки под сообщением правят меню на месте, а нижняя клавиатура (Главная /
Подписка / Ещё) каждый раз присылает новое сообщение — без уборки в чате копились
живые меню, и нажатие в старом перерисовывало его где-то выше по ленте.

Запоминаем последнее меню, которое бот прислал новым сообщением (/start и нижние
кнопки), и удаляем его перед следующим. Никогда не бросает: уборка — не повод
ломать навигацию.
"""

import structlog
from aiogram import Bot

from app.utils.cache import cache


logger = structlog.get_logger(__name__)

# Бот может удалять сообщения в личке только моложе 48 ч — старше и помнить незачем.
NAV_MENU_TTL = 47 * 3600


def _key(chat_id: int) -> str:
    return f'nav_menu:{chat_id}'


async def remember_nav_menu(chat_id: int, message_id: int | None) -> None:
    if not message_id:
        return
    try:
        await cache.set(_key(chat_id), message_id, expire=NAV_MENU_TTL)
    except Exception as error:
        logger.debug('Не удалось запомнить меню чата', chat_id=chat_id, error=str(error))


async def drop_previous_nav_menu(bot: Bot, chat_id: int) -> None:
    try:
        message_id = await cache.getdel(_key(chat_id))
    except Exception as error:
        logger.debug('Не удалось прочитать меню чата', chat_id=chat_id, error=str(error))
        return
    if not message_id:
        return
    try:
        await bot.delete_message(chat_id=chat_id, message_id=int(message_id))
    except Exception as error:  # уже удалено, старше 48 ч — не важно
        logger.debug('Предыдущее меню не удалено', chat_id=chat_id, error=str(error))
