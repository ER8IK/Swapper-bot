from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.inline import main_menu, back_to_menu

router = Router()

WELCOME_MESSAGE = (
    "👋 Hi! Im bot for swap crypto through SimpleSwap.\n\n"
    "⚡ Fast! No registration! No KYC! No limits!\n\n"
    "Choose an action:"
)

HOW_IT_WORKS_TEXT = (
    "📖 <b>How it works:</b>\n\n"
    "1. You choose a currency and amount\n"
    "2. You get the exchange rate\n"
    "3. You confirm — I create the exchange\n"
    "4. You send crypto to the address\n"
    "5. You receive the exchanged coins 🎉\n\n"
    "<i>Powered by SimpleSwap</i>"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=WELCOME_MESSAGE, reply_markup=main_menu())

    
@router.callback_query(F.data == "action_how")
async def callback_how(callback: CallbackQuery):
    await callback.message.edit_text(
        text=HOW_IT_WORKS_TEXT,
        reply_markup=back_to_menu(),
    )
    await callback.answer()
    
@router.callback_query(F.data == "action_back")
async def callback_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_menu(),
    )
