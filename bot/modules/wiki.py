from typing import Optional, List
from telegram import Update
from telegram.ext import CallbackContext
from bot import dispatcher
import wikipedia
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

def wiki(update: Update, context: CallbackContext):
    args = context.args
    reply = " ".join(args)
    summary = '{} {}'
    update.message.reply_text(
        summary.format(
            wikipedia.summary(
                reply,
                sentences=3),
            wikipedia.page(reply).url))


__help__ = """
-> `/wiki` text
Returns search from wikipedia for the input text
"""
__mod_name__ = "Wikipedia"
WIKI_HANDLER = CommandHandler(BotCommands.WikiCommand, wiki, 
                              filters=CustomFilters.authorized_chat, pass_args=True)
dispatcher.add_handler(WIKI_HANDLER)
