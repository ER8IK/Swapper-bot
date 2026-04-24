from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.filters import Command

from database.db import get_user_lang, set_user_lang
from services.i18n import t, TEXTS

router = Router()


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский",  callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English",  callback_data="lang_en"),
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Deutsch",  callback_data="lang_de"),
            InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr"),
        ],
        [
            InlineKeyboardButton(text="🇮🇷 فارسی",    callback_data="lang_fa"),
            InlineKeyboardButton(text="🇸🇦 العربية",  callback_data="lang_ar"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Back",       callback_data="action_back"),  # ← Back button
        ],
    ])


@router.message(Command("language"))
async def cmd_language(message: Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        t(lang, "choose_language"),
        reply_markup=language_keyboard()
    )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]

    if lang not in TEXTS:
        await callback.answer("Unknown language", show_alert=True)
        return

    await set_user_lang(callback.from_user.id, lang)
    await callback.answer()
    await callback.message.edit_text(
        t(lang, "language_set"),
        reply_markup=language_keyboard()
    )