from connection import get_connection


async def create_note(user_id: int, text: str):
    connection = None
    try:
        connection = await get_connection()
        note_id = await connection.fetchval(
            """
            INSERT INTO notes (user_id, text)
            VALUES ($1, $2)
            RETURNING id
            """,
            user_id,
            text
        )
        return note_id
    except Exception as error:
        print(f"Ошибка при создании заметки: {error}")
        raise
    finally:
        if connection:
            await connection.close()


async def get_notes(user_id: int):
    connection = None
    try:
        connection = await get_connection()
        notes = await connection.fetch(
            """
            SELECT id, text
            FROM notes
            WHERE user_id = $1
            ORDER BY id DESC
            """,
            user_id
        )
        return notes
    except Exception as error:
        print(f"Ошибка при получении заметок: {error}")
        raise
    finally:
        if connection:
            await connection.close()


async def get_note(user_id: int, note_id: int):
    connection = None
    try:
        connection = await get_connection()
        note = await connection.fetchrow(
            """
            SELECT id, text
            FROM notes
            WHERE id = $1 AND user_id = $2
            """,
            note_id,
            user_id
        )
        return note
    except Exception as error:
        print(f"Ошибка при получении заметки: {error}")
        raise
    finally:
        if connection:
            await connection.close()


async def update_note(user_id: int, note_id: int, new_text: str):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.execute(
            """
            UPDATE notes
            SET text = $1
            WHERE id = $2 AND user_id = $3
            """,
            new_text,
            note_id,
            user_id
        )
        return result == "UPDATE 1"
    except Exception as error:
        print(f"Ошибка при обновлении заметки: {error}")
        raise
    finally:
        if connection:
            await connection.close()


async def delete_note(user_id: int, note_id: int):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.execute(
            """
            DELETE FROM notes
            WHERE id = $1 AND user_id = $2
            """,
            note_id,
            user_id
        )
        return result == "DELETE 1"
    except Exception as error:
        print(f"Ошибка при удалении заметки: {error}")
        raise
    finally:
        if connection:
            await connection.close()