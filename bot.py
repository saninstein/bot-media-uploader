import os
import tempfile
import uuid

import cv2
import numpy as np
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from config import PHOTO_PATH, TG_BOT_TOKEN, AUDIO_PATH
from utils import has_face, ensure_path, ogg_to_wav_with_sample_rate


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles messages with voice.
    """
    ogg_file_path = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4().hex}.ogg')
    file = await update.message.voice.get_file()
    await file.download_to_drive(ogg_file_path)
    chat_audio_path = ensure_path(AUDIO_PATH, str(update.message.chat_id))
    new_wav_file_path = os.path.join(chat_audio_path, f'audio_message_{len(os.listdir(chat_audio_path))}.wav')
    ogg_to_wav_with_sample_rate(ogg_file_path, new_wav_file_path)
    await update.message.reply_text('Voice saved')


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles messages with photo and save photo with faces to disk
    """
    file = await update.message.photo[-1].get_file()
    img_array = np.asarray(await file.download_as_bytearray(), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    if has_face(img):
        chat_photo_path = ensure_path(PHOTO_PATH, str(update.message.chat_id))
        cv2.imwrite(os.path.join(chat_photo_path, f'{len(os.listdir(chat_photo_path))}.jpg'), img)
        await update.message.reply_text('Has faces')
    else:
        await update.message.reply_text('No faces')

def init_bot():
    """
    Inits the bot
    :return: bot instance
    """
    application = Application.builder().token(TG_BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    return application


def start_bot() -> None:
    """
    Start the bot.
    """
    init_bot().run_polling(allowed_updates=Update.ALL_TYPES)
