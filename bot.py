
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv
import get_pic
import ai
import get_colors
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your command handlers. These usually take the two arguments: bot and update.
def start_command(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Привет! Я твой ассистент по определению цветотипа.\nОтправь мне команду /colourtype и я помогу определить твой цветотип.")

# def help_command(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help! Please tell me how I can assist you.')
    
def colourtype_command(update, context):
    """Send a message when the command /colourtype is issued."""
    update.message.reply_text('Отправь мне фото, а я определю твой цветотип.')
    

def get_color_type(update, context):
    """Process the photo and determine the color type."""
    # Send meassage to the user that proccessing is started
    update.message.reply_text('Определяем ваш цветотип...')
    
    photo = update.message.photo[-1]  # Get the last photo sent by the user
    file_id = photo.file_id
    photo = context.bot.get_file(file_id)
    photo.download('photo.jpg')

    colors = get_colors.get_colors('photo.jpg')

    photo_ans = get_pic.get_colors(colors)

    update.message.reply_photo(photo=open(photo_ans, 'rb'))
    reply = ai.query_openai(ai.create_prompt(colors))
    update.message.reply_text(reply)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    load_dotenv()

    updater = Updater(os.getenv("TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_command))
    # dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("colourtype", colourtype_command))

    # On non-command i.e. message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Log all errors
    dp.add_error_handler(error)

    # Create a handler for photo messages
    dp.add_handler(MessageHandler(Filters.photo, get_color_type))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()