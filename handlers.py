from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

ans_msg = ['Текстовое сообщение получено!', 'We’ve received a message from you!']
ans_voi = ['Голосовое сообщение получено!', 'We’ve received a voice message from you!']
ans_fot = ['Фотография сохранена!', 'Photo saved!']
global lang
lang = 0

# INLINE
# форма inline клавиатуры
inline_frame = [[InlineKeyboardButton("Русский", callback_data=0)],
                [InlineKeyboardButton("English", callback_data=1)]]
# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)


# функция-обработчик команды /start
async def start(update: Update, _):

    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text('Выберите язык:', reply_markup=inline_keyboard)



# функция-обработчик нажатий на кнопки
async def button(update: Update, _):
    # получаем callback query из update
    query = update.callback_query

    # редактируем сообщение после нажатия
    global lang
    lang = int(query.data)
    if lang:
        await query.edit_message_text(text=f"Выбран язык: English")
    else:
        await query.edit_message_text(text=f"Выбран язык: Русский")


# функция-обработчик команды /help
async def help(update, context):
    await update.message.reply_text("Этот бот поддерживает:\n\U0001F539 команду /start - начало работы бота\n\U0001F539 команду /help - помощь\n\U0001F539 текстовые сообщения\n\U0001F539 фотографии\n\U0001F539 голосовые сообщения")


# функция-обработчик текстовых сообщений
async def text(update, context):
    await update.message.reply_text(ans_msg[lang])


# функция-обработчик сообщений с изображениями
async def image(update, context):
    await update.message.reply_text(ans_fot[lang])
    # получаем изображение из апдейта
    file = await update.message.photo[-1].get_file()

    # сохраняем изображение на диск
    await file.download_to_drive("photos/image.jpg")


# функция-обработчик голосовых сообщений
async def voice(update, context):
    # возвращаем пользователю картинку с подписью
    await update.message.reply_photo('images/solar.jpg', caption=ans_voi[lang])


def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

    # добавляем обработчик команды /help
    application.add_handler(CommandHandler("help", help))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с фотографиями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()