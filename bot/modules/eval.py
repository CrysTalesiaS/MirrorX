import io
import os
from functools import wraps
# Common imports for eval
import textwrap
import traceback
from contextlib import redirect_stdout
from bot.helper.telegram_helper.filters import CustomFilters
from bot import LOGGER, dispatcher, OWNER_ID
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, run_async

namespaces = {}


def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
            'effective_message': update.effective_message,
            'effective_user': update.effective_user,
            'effective_chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(
        f"IN: {update.effective_message.text} (user={user}, chat={chat})")


def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(
                chat_id=update.effective_chat.id, document=out_file)
    else:
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{msg}`",
            parse_mode=ParseMode.MARKDOWN)

def dev_plus(func):
    
    @wraps(func)
    def is_dev_plus_func(update: Update, context: CallbackContext, *args,
                         **kwargs):
        bot = context.bot
        user = update.effective_user

        if user.id == OWNER_ID:
            return func(update, context, *args, **kwargs)
        elif not user:
            pass
        else:
            update.effective_message.reply_text(
                "Hanya developer yang bisa jalanin ini command"
                " Kamu gk ada akses buat jalanin nya")

    return is_dev_plus_func
@dev_plus
@run_async
def evaluate(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(eval, bot, update), bot, update)


@dev_plus
@run_async
def execute(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(exec, bot, update), bot, update)


def cleanup_code(code):
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')


def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open(
            os.path.join(os.getcwd(),
                         'bot/modules/temp.txt'),
            'w') as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = f'def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return f'{e.__class__.__name__}: {e}'

    func = env['func']

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
        return f'{value}{traceback.format_exc()}'
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f'{value}'
            else:
                try:
                    result = f'{repr(eval(body, env))}'
                except:
                    pass
        else:
            result = f'{value}{func_return}'
        if result:
            return result


@dev_plus
@run_async
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)


EVAL_HANDLER = CommandHandler(('e', 'ev', 'eva', 'eval'), evaluate,
                              filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
EXEC_HANDLER = CommandHandler(('x', 'ex', 'exe', 'exec', 'py'), execute,
                              filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
CLEAR_HANDLER = CommandHandler('clearlocals', clear,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)

