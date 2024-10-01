import pytest
from databases import BotDB


@pytest.mark.asyncio
async def test_add_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    bot_db = BotDB()

    await bot_db.add_personality(1, "Test Personality", "Description")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    INSERT INTO personalities (creator_id, name, '
        'description)\n'
        '                    VALUES (?, ?, ?)\n'
        '                ',
        (1, 'Test Personality', 'Description')
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    bot_db = BotDB()

    await bot_db.update_personality(1, "Updated Name", "Updated Description")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    UPDATE personalities\n'
        '                    SET name = ?, description = ?\n'
        '                    WHERE id = ?\n'
        '                ',
        ('Updated Name', 'Updated Description', 1)
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    bot_db = BotDB()

    await bot_db.delete_personality(1)

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    DELETE FROM personalities\n'
        '                    WHERE id = ?\n'
        '                ',
        (1,)
    )
    mock_conn.commit.assert_called_once()
