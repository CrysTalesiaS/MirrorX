import shutil, psutil
import os
import html 
import subprocess
import signal
import platform
from platform import python_version
import pickle
from bot import app
from threading import Thread
from os import execl, path, remove
from sys import executable
import datetime
import pytz
from telethon import events
from datetime import datetime
from pyrogram import idle
from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from telegram import ParseMode, __version__, InlineKeyboardButton
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, extra, list, wiki, paste, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, anime, stickers, search, delete, speedtest, usage
from bot.modules.alternate import typing_action

now=datetime.now(pytz.timezone('Asia/Jakarta'))
_IS_TELEGRAPH = True
_IS_STICKER = True

_DEFAULT = "https://t.me/c/1475139935/22255"
_CHAT, _MSG_ID = None, None
_LOGO_ID = https://t.me/c/1475139935/22255

@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    current = now.strftime('%Y/%m/%d %I:%M:%S')
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Bot Menyala Sejak⌚:</b> {currentTime}\n' \
            f'<b>Sisa Penyimpanan🗄️:</b> {total}\n' \
            f'<b>Memory bot terpakai🗃️:</b> {used}  ' \
            f'<b>Ruang Kosong Bot🗃️:</b> {free}\n' \
            f'<b>Waktu bot menyala pertama kali👨‍💻:</b> {current}\n\n' \
            f'📇Pengunaan data bot📇\n<b>Kouta Ter Upload :</b> {sent}\n' \
            f'<b>Kouta Ter Download:</b> {recv}\n\n' \
            f'<b>CPU 🖥️:</b> {cpuUsage}% ' \
            f'<b>RAM ⛏️:</b> {memory}% ' \
            f'<b>Penyimpanan 🗄️:</b> {disk}%'
    sendMessage(stats, context.bot, update)










    

@run_async
def start(update, context):
    start_string = f'''
Hay,aku [Aulia](t.me/AnnisaAwlia), yuk ikut grup mirror aku [Kaca/Mirror](t.me/BotMirror)
Ketik /{BotCommands.HelpCommand} biar bisa liat perintah bot
'''
    update.effective_message.reply_photo("https://telegra.ph/file/583c0e1fc0e4931d6ce56.jpg", start_string, parse_mode=ParseMode.MARKDOWN)



@run_async
def restart(update, context):
    restart_message = sendMessage("Bentar lagi restart", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)
    
@run_async
def systemstats(update, context):
    uname = platform.uname()
    system = platform.system()
    
    code = f'<b>======[ SYSTEM INFO ]======</b>\n\n' \
             f'<b>System:</b> <code>' + str(uname.system) + '</code>\n' \
             f'<b>Node name:</b> <code>' + str(uname.node) + '</code>\n' \
             f'<b>Release:</b> <code>' + str(uname.release) + '</code>\n' \
             f'<b>Version:</b> <code>' + str(uname.version) + '</code>\n' \
             f'<b>Machine:</b> <code>' + str(uname.machine) + '</code>\n' \
             f'<b>Processor:</b> <code>' + str(uname.processor) + '</code>\n' \
             f'<b>Python version:</b> <code>' + python_version() + '</code>\n' \
             f'<b>Library version:</b> <code>' + str(__version__) + '</code>\n'
    context.bot.sendMessage(
        update.effective_chat.id, code, parse_mode=ParseMode.HTML
       )
    update.effective_message.reply_photo("https://telegra.ph/file/b783e7e79d76c7310e79d.jpg", code, parse_mode=ParseMode.MARKDOWN)
    
@run_async
def userbot_help(update, context):
    userbot_string = f'''
──「 *Corona:* 」──
-> `/covid`
To get Global data
-> `/covid` <country>
To get data of a country
──「 *Urban Dictionary:* 」──
-> `/ud` <word>: Type the word or expression you want to search use.
──「 *Currency Converter:* 」──
Example syntax: `/cash 1 USD INR`
-> `/cash`
currency converter
──「 *Wallpapers:* 」──
-> `/wall` <query>
get a wallpaper from wall.alphacoders.com
──「 *Google Reverse Search:* 」──
-> `/reverse`
Does a reverse image search of the media which it was replied to.
──「 *Text-to-Speach* 」──
-> `/tts` <sentence>
Text to Speech!
──「 *Last FM:* 」──
-> `/setuser` <username>
sets your last.fm username.
-> `/clearuser`
removes your last.fm username from the bot's database.
-> `/lastfm`
returns what you're scrobbling on last.fm.
──「 *Playstore:* 」──
-> `/app` <app name>
finds an app in playstore for you
-> `/wiki` text
Returns search from wikipedia for the input text
-> `/tr` (language code)
Translates Languages to a desired Language code.
'''
    sendMessage(userbot_string, context.bot, update)
    
@run_async
def bot_help(update, context):
    help_string = f'''
/mirror : ngeliat help dari commit mirrot

/userbot : ngeliat help dari commit userbot/bot manajer

'''
    sendMessage(help_string, context.bot, update)

    
@run_async
def mirror_help(update, context):
    mirror_string = f'''
/{BotCommands.HelpCommand}: Tutor botnya

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Mulai Mirror bot dengan perintah /kaca (link mega/google drive/zippy/mediafire)

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link] : Sama kayak perintah mirror tapi bedanya ini langsung di ekstrak

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Sama kayak perintah mirror tapi bedanya ini menjadikan file ekstensi .tar

/{BotCommands.WatchCommand} [youtube-dl supported link]: Nge download video dari youtube. Click /{BotCommands.WatchCommand} for more help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Sama kayak perintah watch tp bedanya ini diubah ke ekstensi .tar

/{BotCommands.CancelMirror} : Ngebatalin Mirror

/{BotCommands.StatusCommand}: Ngeliat status mirror

/{BotCommands.ListCommand} [search term]: Mencari list di google drive

/{BotCommands.StatsCommand}: Menampilkan system bot

/{BotCommands.AuthorizeCommand}: Supaya bot bisa digunain oleh orang lain/grup

/{BotCommands.LogCommand}: Log bot 

/{BotCommands.SpeedCommand} : Cek kecepatan internet

/{BotCommands.CloneCommand} : Clone link Google Drive

/{BotCommands.SystemstatsCommand} : Ngeliat system yang dipakai bot saat ini

/{BotCommands.UsageCommand}: ngeliat sisa penggunaan bulan ini

/{BotCommands.WikiCommand} : Testing commit. wikipedia search

/{BotCommands.TotranslateCommand} : Testing commit. translate a word

/{BotCommands.PasteCommand} : Testing Commit. paste a word to neko.bin

/{BotCommands.systemkutestCommand} : testing commit. just show neofetch

/tolongturrent: buat nyari link torrent

/wibu: buat nyari anime,manga 

/tolongstiker: buat bikin stiker

/Eval : Eval sebuah code line(python) dengan : ('e', 'ev', 'eva', 'eval')

/Execute : Execute sebuah command(python) dengan : ('x', 'ex', 'exe', 'exec', 'py')

/clearlocals : clear lokal, idk what this command. u can try ur self

'''
    sendMessage(mirror_string, context.bot, update)
    
@run_async
def _get_alive_text_and_markup(message: Message) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    markup = None
    output = f"""
**⏱ Uptime** : `{userge.uptime}`
**💡 Version** : `{get_version()}`
**__Python__**: `{versions.__python_version__}`
    **__Pyrogram__**: `{versions.__pyro_version__}`"""
    

async def _send_alive(message: Message,
                      text: str,
                      reply_markup: Optional[InlineKeyboardMarkup],
                      recurs_count: int = 0) -> None:
    if not _LOGO_ID:
        await _refresh_id(message)
    should_mark = None if _IS_STICKER else reply_markup
    if _IS_TELEGRAPH:
        await _send_telegraph(message, text, reply_markup)
    else:
        try:
            await message.client.send_cached_media(chat_id=message.chat.id,
                                                   file_id=_LOGO_ID,
                                                   caption=text,
                                                   reply_markup=should_mark)
            if _IS_STICKER:
                raise ChatSendMediaForbidden
        except SlowmodeWait as s_m:
            await asyncio.sleep(s_m.x)
            text = f'<b>{str(s_m).replace(" is ", " was ")}</b>\n\n{text}'
            return await _send_alive(message, text, reply_markup)
        except MediaEmpty:
            if recurs_count >= 2:
                raise ChatSendMediaForbidden
            await _refresh_id(message)
            return await _send_alive(message, text, reply_markup, recurs_count + 1)
        except (ChatSendMediaForbidden, Forbidden):
            await message.client.send_message(chat_id=message.chat.id,
                                              text=text,
                                              disable_web_page_preview=True,
                                              reply_markup=should_mark)
            
                       

async def _refresh_id(message: Message) -> None:
    global _LOGO_ID, _IS_STICKER  # pylint: disable=global-statement
    try:
        media = await message.client.get_messages(_CHAT, _MSG_ID)
    except (ChannelInvalid, PeerIdInvalid, ValueError):
        _set_data(True)
        return await _refresh_id(message)
    else:
        if media.sticker:
            _IS_STICKER = True
        _LOGO_ID = get_file_id_of_media(media)
        
def _set_data(errored: bool = False) -> None:
    global _CHAT, _MSG_ID, _IS_TELEGRAPH  # pylint: disable=global-statement

    pattern_1 = r"^(http(?:s?):\/\/)?(www\.)?(t.me)(\/c\/(\d+)|:?\/(\w+))?\/(\d+)$"
    pattern_2 = r"^https://telegra\.ph/file/\w+\.\w+$"
    if Config.ALIVE_MEDIA and not errored:
        if Config.ALIVE_MEDIA.lower().strip() == "nothing":
            _CHAT = "text_format"
            _MSG_ID = "text_format"
            return
        media_link = Config.ALIVE_MEDIA
        match_1 = re.search(pattern_1, media_link)
        match_2 = re.search(pattern_2, media_link)
        if match_1:
            _MSG_ID = int(match_1.group(7))
            if match_1.group(5):
                _CHAT = int("-100" + match_1.group(5))
            elif match_1.group(6):
                _CHAT = match_1.group(6)
        elif match_2:
            _IS_TELEGRAPH = True
        elif "|" in Config.ALIVE_MEDIA:
            _CHAT, _MSG_ID = Config.ALIVE_MEDIA.split("|", maxsplit=1)
            _CHAT = _CHAT.strip()
            _MSG_ID = int(_MSG_ID.strip())
    else:
        match = re.search(pattern_1, _DEFAULT)
        _CHAT = match.group(6)
        _MSG_ID = int(match.group(7))


async def _send_telegraph(msg: Message, text: str, reply_markup: Optional[InlineKeyboardMarkup]):
    path = os.path.join(Config.DOWN_PATH, os.path.split(Config.ALIVE_MEDIA)[1])
    if not os.path.exists(path):
        await pool.run_in_thread(wget.download)(Config.ALIVE_MEDIA, path)
    if path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
        await msg.client.send_photo(
            chat_id=msg.chat.id,
            photo=path,
            caption=text,
            reply_markup=reply_markup
        )
    elif path.lower().endswith((".mkv", ".mp4", ".webm")):
        await msg.client.send_video(
            chat_id=msg.chat.id,
            video=path,
            caption=text,
            reply_markup=reply_markup
        )
    else:
        await msg.client.send_document(
            chat_id=msg.chat.id,
            document=path,
            caption=text,
            reply_markup=reply_markup
        )
    
def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter| CustomFilters.authorized_user)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    system_handler = CommandHandler(BotCommands.SystemstatsCommand, systemstats,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)




    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(system_handler)

    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
