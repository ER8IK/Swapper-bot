from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.inline import main_menu, back_to_menu
from database.db import get_user_lang, set_user_lang
from services.i18n import t

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        text=t(lang, "welcome"),
        reply_markup=main_menu(lang)
    )


@router.callback_query(F.data == "action_how")
async def callback_how(callback: CallbackQuery):
    await callback.answer()
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        text=t(lang, "how_it_works"),
        reply_markup=back_to_menu(lang)
    )


@router.callback_query(F.data == "action_back")
async def callback_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        text=t(lang, "welcome"),
        reply_markup=main_menu(lang)
    )


@router.callback_query(F.data == "action_language")
async def callback_language(callback: CallbackQuery):
    await callback.answer()
    from handlers.language import language_keyboard
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        text=t(lang, "choose_language"),
        reply_markup=language_keyboard()
    )