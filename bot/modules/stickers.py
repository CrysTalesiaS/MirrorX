import os
import re
import math
import requests
import urllib.request as urllib
from PIL import Image
from html import escape
from bs4 import BeautifulSoup as bs

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError, Update
from telegram.ext import run_async, CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

from bot import dispatcher

combot_stickers_url = "https://combot.org/telegram/stickers?q="


@run_async
def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello " +
            f"{mention_html(msg.from_user.id, msg.from_user.first_name)}" +
            ", Id pesan yang kamu balas :\n <code>" +
            escape(msg.reply_to_message.sticker.file_id) + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello " +
            f"{mention_html(msg.from_user.id, msg.from_user.first_name)}" +
            ", Balas Pesan sticker yang kamu pengen dapetin id nya",
            parse_mode=ParseMode.HTML,
        )


@run_async
def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(' ', 1)
    if len(split) == 1:
        msg.reply_text('Bentar lagi bikin nama buat stickernya.')
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, 'lxml')
    results = soup.find_all("a", {'class': "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text('Stiker gk ada :(.')
        return
    reply = f"Sticker buat *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result['href']
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.png")
        bot.send_document(chat_id, document=open("sticker.png", "rb"))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text(
            "Balaskan ke sticker niscaya akan ku ubah ke PNG.")


@run_async
def kang(update: Update, context: CallbackContext):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = ("a" + str(packnum) + "_" + str(user.id) + "_by_" +
                            context.bot.username)
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Sticker invalid nih":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("Yah itu sticker gak bisa di kang :(")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"

        if not is_animated:
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"Sticker nya udah kutambah ke [pack](t.me/addstickers/{packname})"
                    + f"\nEmot nya : {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )

            except OSError as e:
                msg.reply_text("Aku bisanya kang/nyuri foto doang.")
                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid nih":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    msg.reply_text(
                        f"Sticker berhasil ditambah kan ke[pack](t.me/addstickers/{packname})"
                        + f"\nEmotnya : {sticker_emoji}",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Emotnya gak bisa nih":
                    msg.reply_text("Emot gk bisa(s).")
                elif e.message == "Stickers nya kebanyakan":
                    msg.reply_text(
                        "Kegedean fike nya -_-")
                elif e.message == "Stikernya gk ada (500)":
                    msg.reply_text(
                        "Sticker berhasil ditambahin ke[pack](t.me/addstickers/%s)"
                        % packname + "\n"
                        "Emotnya :" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = ("animated" + str(packnum) + "_" +
                                    str(user.id) + "_by_" +
                                    context.bot.username)
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid nih":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"Sticker berhasil ditambahin ke [pack](t.me/addstickers/{packname})"
                    + f"\nEmotnya : {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                elif e.message == "Emotnya gak bisa nih":
                    msg.reply_text("Emotnya gk bisa nih(s).")
                elif e.message == "Stikernya gk ada (500)":
                    msg.reply_text(
                        "Sticker berhasil ditambah ke [pack](t.me/addstickers/%s)"
                        % packname + "\n"
                        "Emotnya :" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🤔"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            msg.reply_text(
                f"Sticker berhasil ditambah ke [pack](t.me/addstickers/{packname})"
                + f"\nEmotnya : {sticker_emoji}",
                parse_mode=ParseMode.MARKDOWN,
            )
        except OSError as e:
            msg.reply_text("I can only kang images m8.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    "Sticker berhasil ditambah ke [pack](t.me/addstickers/%s)"
                    % packname + "\n" + "Emotnya :" + " " + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            elif e.message == "Emotnya gk bisa tau":
                msg.reply_text("Emotnya gk bisa tau(s).")
            elif e.message == "Stickernya kebanyakan":
                msg.reply_text("Filenya kegedean nih :( gk bisa dijadiin stiker")
            elif e.message == "Stiker gk ada(500)":
                msg.reply_text(
                    "Sticker udah berhasil ditambah ke [pack](t.me/addstickers/%s)"
                    % packname + "\n"
                    "Emotnya :" + " " + sticker_emoji,
                    parse_mode=ParseMode.MARKDOWN,
                )
            print(e)
    else:
        packs = "Balas sebuah pesan Stiker/Foto niscaya akan ku jadikan stiker\nOiya btw ni stikernya:\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        msg.reply_text(packs, parse_mode=ParseMode.MARKDOWN)
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")
    elif os.path.isfile("kangsticker.tgs"):
        os.remove("kangsticker.tgs")


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s kang pack" + extra_version,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s animated kang pack" + extra_version,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Stikernya udah ada":
            msg.reply_text(
                "Stikermu  bisa digunain disini[here](t.me/addstickers/%s)" % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        elif e.message in ("Peer_id_invalid", "botnya di udah diblok sama ownernya"):
            msg.reply_text(
                "Kontak @AnnisaAwlia dulu.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text="Start", url=f"t.me/{context.bot.username}")
                ]]),
            )
        elif e.message == "Bikin stikernya gak bisa (500)":
            msg.reply_text(
                "Sticker kamu udh berhasil ditambahin ke sini [here](t.me/addstickers/%s)"
                % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        return

    if success:
        msg.reply_text(
            "Sticker kamu udh berhasil ditambahin ke sini[here](t.me/addstickers/%s)"
            % packname,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        msg.reply_text(
            "Failed to create sticker pack. Possibly due to blek mejik.")


@run_async
def stickhelp(update, context):
    help_string = '''
• `/idstiker`*:* Balas pesan stiker buat nyari id stikernya
• `/dapatstiker`*:* balas ke pesan stiker buat ku upload jadi PNG/Foto
• `/curry`*:* balas sebuah pesan stiker nanti aku curry hehe ><
• `/sticker`*:* Cari stiker yang kamu pengen
'''
    update.effective_message.reply_photo("https://telegra.ph/file/db03910496f06094f1f7a.jpg", help_string, parse_mode=ParseMode.MARKDOWN)

STICKERID_HANDLER = CommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = CommandHandler("getsticker", getsticker)
KANG_HANDLER = CommandHandler("kang", kang)
STICKERS_HANDLER = CommandHandler("stickers", cb_sticker)
STICKHELP_HANDLER = CommandHandler("stickerhelp", stickhelp)


dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(STICKHELP_HANDLER)
