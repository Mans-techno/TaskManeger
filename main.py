import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from connection import create_database
from service import *
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")


bot = Bot(token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    try:
        name = message.from_user.first_name or "друг"
        await message.answer(f"""
Привет {name} 👋

Команды:
➕ /create — создать заметку
📋 /list — посмотреть заметки
🔎 /read — открыть заметку
✏️ /update — изменить заметку
🗑️ /delete — удалить заметку
❓ /help — помощь
        """)
    except Exception as error:
        print(f"Erorr with /start: {error}")


@dp.message(Command("help"))
async def help_handler(message: Message):
    try:
        await message.answer(f"""
Вот несколько примеров 👇
Создать:
/create Купить продукты
Посмотреть все:
/list
Открыть одну заметку:
/read 1
Изменить:
/update 1 Купить продукты вечером
Удалить:
/delete 1
        """)
    except Exception as error:
        print(f"Error with /help: {error}")


@dp.message(Command("create"))
async def create_handler(message: Message):
    try:
        text = message.text.partition(" ")[2].strip()
        if not text:
            await message.answer(f"""
После /create нужно написать текст заметки 🙂
Например: /create Сделать домашнее задание
            """)
            return
        note_id = await create_note(
            message.from_user.id,
            text
        )

        await message.answer(f"""
Заметка сохранена ✅
ID: {note_id}
📝 {text}
        """)
    except Exception as error:
        print(f"Error with /create: {error}")
        await message.answer("Не получилось сохранить заметку")


@dp.message(Command("list"))
async def list_handler(message: Message):
    try:
        notes = await get_notes(message.from_user.id)
        if not notes:
            await message.answer("Заметок пока нет 🙂")
            return
        result = "Твои заметки 📋\n\n"
        for note in notes:
            result += f"#{note['id']} — {note['text']}\n"
        await message.answer(result)

    except Exception as error:
        print(f"Error with /list: {error}")
        await message.answer("Не получилось загрузить заметки. Попробуй ещё раз.")



@dp.message(Command("read"))
async def read_handler(message: Message):
    try:
        value = message.text.partition(" ")[2].strip()
        if not value.isdigit():
            await message.answer("Укажи ID заметки например: /read 3")
            return
        note = await get_note(
            message.from_user.id,
            int(value)
        )
        if not note:
            await message.answer(f"""
Заметки с таким id нету 🤔
Посмотреть список можно через /list.
            """)
            return

        await message.answer(f"""
Заметка #{note['id']}
📝 {note['text']}
            """)
        
    except Exception as error:
        print(f"Error with /read: {error}")
        await message.answer("Не получилось открыть заметку. Попробуй ещё раз.")



@dp.message(Command("update"))
async def update_handler(message: Message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer(f"""
Укажи ID и новый текст
Например: /update 2 Позвонить другу вечером
            """)
            return
        note_id = parts[1]
        new_text = parts[2].strip()
        
        if not note_id.isdigit():
            await message.answer("ID заметки должен быть числом")
            return
        updated = await update_note(
            message.from_user.id,
            int(note_id),
            new_text
        )

        if not updated:
            await message.answer(f"""Не нашёл заметку с таким id 🤔""")
            return
        await message.answer(f"""
            Готово, заметка обновлена ✏️
            📝 {new_text}
    """)
    except Exception as error:
        print(f"Error with /update: {error}")
        await message.answer("Не получилось изменить заметку. Попробуй ещё раз.")



@dp.message(Command("delete"))
async def delete_handler(message: Message):
    try:
        value = message.text.partition(" ")[2].strip()
        if not value.isdigit():
            await message.answer(f"""
Укажи ID заметки
Например: /delete 4
            """)
            return
        deleted = await delete_note(
            message.from_user.id,
            int(value)
        )

        if not deleted:
            await message.answer("Заметку с таким ID я не нашёл")
            return

        await message.answer("Заметка удалена 🗑️")
    except Exception as error:
        print(f"Error with /delete: {error}")
        await message.answer("Не получилось удалить заметку. Попробуй ещё раз.")



@dp.message(F.text)
async def unknown_handler(message: Message):
    try:
        await message.answer(f"""
Не совсем понял тебя 😅
Напиши /help, чтобы посмотреть команды
        """)

    except Exception as error:
        print(f"Error: {error}")




async def main():
    try:
        await create_database()
        print("Connection Successful")
        print("Bot started")
        await dp.start_polling(bot)
    except Exception as error:
        print(f"Error with connection: {error}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())