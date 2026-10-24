from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from app.services.referral_contest_service import ReferralContestService, mask_public_name


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('Вася Пупкин', 'Ва***'),
        ('Ян', 'Я***'),
        ('@kvaken_fan', 'kv***'),
        ('123456789', 'Участник'),
        ('', 'Участник'),
        (None, 'Участник'),
    ],
)
def test_mask_public_name(name, expected):
    assert mask_public_name(name) == expected


def _contest():
    return SimpleNamespace(title='Конкурс', prize_text=None, end_at=datetime.now(UTC))


async def _post(leaderboard, *, is_final):
    service = ReferralContestService()
    service.bot = SimpleNamespace(send_message=AsyncMock())
    with patch(
        'app.services.channel_subscription_service.channel_subscription_service.get_first_channel_id',
        AsyncMock(return_value='-100'),
    ):
        await service._notify_public_channel(
            contest=_contest(),
            leaderboard=leaderboard,
            total_events=0,
            today_events=0,
            is_final=is_final,
            tz=ZoneInfo('Europe/Moscow'),
        )
    return service.bot.send_message


async def test_public_post_masks_names_and_hides_timezone():
    send = await _post([('Вася Пупкин', 7, 0, False)], is_final=False)
    text = send.await_args.kwargs['text']
    assert 'Ва***' in text
    assert 'Пупкин' not in text
    assert 'Europe/Moscow' not in text


async def test_empty_intermediate_post_skipped():
    send = await _post([], is_final=False)
    send.assert_not_awaited()
