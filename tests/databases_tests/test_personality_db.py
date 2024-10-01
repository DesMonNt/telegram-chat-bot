import pytest
from databases import PersonalityDB


@pytest.mark.asyncio
async def test_init_db(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    db = PersonalityDB()

    await db.init_db()

    mock_conn.execute.assert_any_call(
        '\n'
        '                CREATE TABLE IF NOT EXISTS user_settings (\n'
        '                    user_id INTEGER PRIMARY KEY,\n'
        '                    active_personality TEXT\n'
        '                )\n'
        '            '
    )
    mock_conn.execute.assert_any_call(
        '\n'
        '                CREATE TABLE IF NOT EXISTS user_settings (\n'
        '                    user_id INTEGER PRIMARY KEY,\n'
        '                    active_personality TEXT\n'
        '                )\n'
        '            '
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_add_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    db = PersonalityDB()

    await db.add_personality(1, "Test Personality", "Description")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    INSERT INTO personalities (user_id, name, description)\n'
        '                    VALUES (?, ?, ?)\n'
        '                ',
        (1, 'Test Personality', 'Description')
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    db = PersonalityDB()

    await db.update_personality(1, "Test Personality", "Updated Description")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    UPDATE personalities\n'
        '                    SET description = ?\n'
        '                    WHERE user_id = ? AND name = ?\n'
        '                ',
         ('Updated Description', 1, 'Test Personality')
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    db = PersonalityDB()

    await db.delete_personality(1, "Test Personality")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    DELETE FROM personalities\n'
        '                    WHERE user_id = ? AND name = ?\n'
        '                ',
        (1, 'Test Personality')
    )
    mock_conn.commit.assert_called_once()


@pytest.mark.asyncio
async def test_set_active_personality(mocker):
    mock_db = mocker.patch("aiosqlite.connect")
    mock_conn = mock_db.return_value.__aenter__.return_value

    db = PersonalityDB()

    await db.set_active_personality(1, "Test Personality")

    mock_conn.execute.assert_called_once_with(
        '\n'
        '                    INSERT INTO user_settings (user_id, active_personality)\n'
        '                    VALUES (?, ?)\n'
        '                    ON CONFLICT(user_id) DO UPDATE SET active_personality = '
        '?\n'
        '                ',
        (1, 'Test Personality', 'Test Personality')
    )
    mock_conn.commit.assert_called_once()
