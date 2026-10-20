"""Навигация: нижняя клавиатура повторяет главное меню, «Назад» ведёт на уровень выше."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.keyboards.inline import (
    get_balance_keyboard,
    get_info_menu_keyboard,
    get_language_selection_keyboard,
    get_main_menu_keyboard,
    get_more_menu_keyboard,
    get_referral_keyboard,
    get_support_keyboard,
)
from app.keyboards.reply import get_nav_reply_keyboard, legacy_nav_menu_labels, nav_menu_labels
from app.utils import nav_menu


def _last_callback(markup):
    return markup.inline_keyboard[-1][-1].callback_data


def _callbacks(markup):
    return [button.callback_data for row in markup.inline_keyboard for button in row if button.callback_data]


def test_bottom_keyboard_mirrors_main_menu_sections():
    texts = [button.text for button in get_nav_reply_keyboard('ru').keyboard[0]]
    assert texts == ['Главная', 'Подписка', 'Ещё']
    assert all(button.icon_custom_emoji_id for button in get_nav_reply_keyboard('ru').keyboard[0])


def test_main_menu_subscription_button_named_like_bottom_key():
    markup = get_main_menu_keyboard('ru', has_active_subscription=True, subscription_is_active=True)
    by_callback = {b.callback_data: b for row in markup.inline_keyboard for b in row if b.callback_data}
    assert by_callback['menu_subscription'].text == 'Подписка'
    assert by_callback['menu_more'].text == 'Ещё'
    assert by_callback['menu_more'].icon_custom_emoji_id


def test_legacy_labels_differ_from_current():
    assert set(legacy_nav_menu_labels('ru').values()).isdisjoint(nav_menu_labels('ru').values())


@pytest.mark.parametrize(
    'markup',
    [
        get_balance_keyboard('ru'),
        get_referral_keyboard('ru'),
        get_support_keyboard('ru'),
        get_info_menu_keyboard('ru'),
    ],
    ids=['balance', 'referrals', 'support', 'info'],
)
def test_screens_opened_from_more_go_back_to_more(markup):
    assert _last_callback(markup) == 'menu_more'


def test_more_menu_itself_goes_back_to_main():
    assert _last_callback(get_more_menu_keyboard('ru')) == 'back_to_menu'


def test_language_back_target_is_configurable():
    assert _last_callback(get_language_selection_keyboard(include_back=True)) == 'back_to_menu'
    markup = get_language_selection_keyboard(include_back=True, back_callback='menu_more')
    assert _last_callback(markup) == 'menu_more'


async def test_drop_previous_menu_deletes_remembered_message():
    bot = MagicMock()
    bot.delete_message = AsyncMock()
    with patch.object(nav_menu, 'cache') as cache:
        cache.getdel = AsyncMock(return_value=42)
        await nav_menu.drop_previous_nav_menu(bot, 100)
    bot.delete_message.assert_awaited_once_with(chat_id=100, message_id=42)


async def test_drop_previous_menu_without_remembered_message_is_noop():
    bot = MagicMock()
    bot.delete_message = AsyncMock()
    with patch.object(nav_menu, 'cache') as cache:
        cache.getdel = AsyncMock(return_value=None)
        await nav_menu.drop_previous_nav_menu(bot, 100)
    bot.delete_message.assert_not_awaited()


async def test_drop_previous_menu_swallows_telegram_errors():
    bot = MagicMock()
    bot.delete_message = AsyncMock(side_effect=RuntimeError('message to delete not found'))
    with patch.object(nav_menu, 'cache') as cache:
        cache.getdel = AsyncMock(return_value=42)
        await nav_menu.drop_previous_nav_menu(bot, 100)  # не бросает


async def test_remember_menu_ignores_empty_id():
    with patch.object(nav_menu, 'cache') as cache:
        cache.set = AsyncMock()
        await nav_menu.remember_nav_menu(100, None)
        cache.set.assert_not_awaited()
        await nav_menu.remember_nav_menu(100, 7)
        cache.set.assert_awaited_once()
