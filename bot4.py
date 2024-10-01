import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from config import TOKEN

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем клавиатуру для задания 1
hi_button = KeyboardButton(text='Привет')  # исправлено
bye_button = KeyboardButton(text='Пока')  # исправлено
keyboard = ReplyKeyboardMarkup(
    keyboard=[[hi_button, bye_button]],  # кнопки передаем в виде списка списков
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message):
    await message.answer("Выберите опцию:", reply_markup=keyboard)

# Обработчики для кнопок "Привет" и "Пока"
@dp.message(F.text == 'Привет')
async def greet_user(message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == 'Пока')
async def say_goodbye(message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2: Кнопки с URL-ссылками
@dp.message(Command('links'))
async def show_links(message):
    # Создаем инлайн-кнопки с URL-ссылками
    news_button = InlineKeyboardButton(text="Новости", url="https://news.example.com")
    music_button = InlineKeyboardButton(text="Музыка", url="https://music.example.com")
    video_button = InlineKeyboardButton(text="Видео", url="https://video.example.com")

    # Добавляем кнопки в клавиатуру (в виде списка списков кнопок)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[news_button], [music_button], [video_button]])

    await message.answer("Вот ссылки:", reply_markup=keyboard)


# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command('dynamic'))
async def show_dynamic_keyboard(message):
    # Кнопка "Показать больше"
    show_more_button = InlineKeyboardButton(text="Показать больше", callback_data="show_more")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[show_more_button]])

    await message.answer("Нажмите кнопку для показа дополнительных опций.", reply_markup=keyboard)


# Обработка нажатия на кнопку "Показать больше"
@dp.callback_query(lambda c: c.data == "show_more")
async def show_options(callback_query: CallbackQuery):
    # Заменяем кнопку "Показать больше" на две новые кнопки
    option1_button = InlineKeyboardButton(text="Опция 1", callback_data="option_1")
    option2_button = InlineKeyboardButton(text="Опция 2", callback_data="option_2")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[option1_button], [option2_button]])

    await callback_query.message.edit_text("Выберите опцию:", reply_markup=keyboard)


# Обработка нажатий на кнопки "Опция 1" и "Опция 2"
@dp.callback_query(lambda c: c.data in ["option_1", "option_2"])
async def process_option(callback_query: CallbackQuery):
    option_text = "Вы выбрали Опцию 1" if callback_query.data == "option_1" else "Вы выбрали Опцию 2"

    await callback_query.message.edit_text(option_text)

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

