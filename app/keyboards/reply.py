from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from app.config import settings
from app.localization.texts import get_texts


def get_main_reply_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)

    keyboard = [[KeyboardButton(text=texts.MENU_BALANCE), KeyboardButton(text=texts.MENU_SUBSCRIPTION)]]

    # Добавляем кнопки промокода и рефералов, учитывая настройки
    second_row = [KeyboardButton(text=texts.MENU_PROMOCODE)]

    # Добавляем кнопку рефералов только если программа включена
    if settings.is_referral_program_enabled():
        second_row.append(KeyboardButton(text=texts.MENU_REFERRALS))

    keyboard.append(second_row)

    keyboard.append([KeyboardButton(text=texts.MENU_SUPPORT), KeyboardButton(text=texts.MENU_RULES)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)


def nav_menu_labels(language: str = 'ru') -> dict[str, str]:
    """Single source of truth for the persistent nav reply-keyboard labels.

    Both the keyboard buttons and the message-text filters that route them are
    built from this dict, so the button caption and the filter can never drift.
    Inline defaults are used so the labels render even when a mounted runtime
    locale file omits the keys (see locales mount override on the stand).
    """
    texts = get_texts(language)
    return {
        'profile': texts.t('REPLY_MENU_PROFILE', '👤 Профиль'),
        'subscription': texts.t('MENU_SUBSCRIPTION', '📱 Подписка'),
        'info': texts.t('MENU_INFO', 'ℹ️ Инфо'),
    }


def get_nav_reply_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    """Persistent bottom reply-keyboard with the three main-menu shortcuts."""
    labels = nav_menu_labels(language)
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels['profile'], style='success'),
                KeyboardButton(text=labels['subscription'], style='success'),
                KeyboardButton(text=labels['info'], style='success'),
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        one_time_keyboard=False,
    )


def get_admin_reply_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.ADMIN_USERS), KeyboardButton(text=texts.ADMIN_SUBSCRIPTIONS)],
            [KeyboardButton(text=texts.ADMIN_PROMOCODES), KeyboardButton(text=texts.ADMIN_MESSAGES)],
            [KeyboardButton(text=texts.ADMIN_STATISTICS), KeyboardButton(text=texts.ADMIN_MONITORING)],
            [KeyboardButton(text=texts.t('ADMIN_MAIN_MENU', '🏠 Главное меню'))],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_cancel_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts.CANCEL)]], resize_keyboard=True, one_time_keyboard=True
    )


def get_confirmation_reply_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts.YES), KeyboardButton(text=texts.NO)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_skip_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts.REFERRAL_CODE_SKIP)]], resize_keyboard=True, one_time_keyboard=True
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def get_contact_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.t('SEND_CONTACT_BUTTON', '📱 Отправить контакт'), request_contact=True)],
            [KeyboardButton(text=texts.CANCEL)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_location_keyboard(language: str = 'ru') -> ReplyKeyboardMarkup:
    texts = get_texts(language)
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.t('SEND_LOCATION_BUTTON', '📍 Отправить геолокацию'), request_location=True)],
            [KeyboardButton(text=texts.CANCEL)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
