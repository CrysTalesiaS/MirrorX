import requests
from telegram import Update, ParseMode
from telegram.ext import run_async, CallbackContext

from bot import dispatcher

from telegram.ext import CommandHandler
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters


@run_async
def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text

    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?")
        return

    key = requests.post('https://nekobin.com/api/documents',
                        json={"content": data}).json().get('result').get('key')
    url = f'https://nekobin.com/{key}'
    reply_text = f'Nekofied to *Nekobin* : {url}'
    message.reply_text(
        reply_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True)


__help__ = """
-> `/paste`
Do a paste at `neko.bin`
"""

PASTE_HANDLER = CommandHandler(BotCommands.PasteCommand, paste, 
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, pass_args=True)
dispatcher.add_handler(PASTE_HANDLER)

__mod_name__ = "Paste"
__command_list__ = ["paste"]
__handlers__ = [PASTE_HANDLER]
