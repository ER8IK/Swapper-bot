"""
AML (Anti-Money Laundering) agreement handler.
User must accept before making their first swap.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database.db import accept_aml, get_user_lang
from services.i18n import t

router = Router()

AML_TEXT = """
⚖️ <b>AML Policy Agreement</b>

Before using this service, please read and accept our Anti-Money Laundering policy.

By using this bot you confirm that:

1. You are the legal owner of the funds being exchanged.
2. The funds do not originate from illegal activities.
3. You are not on any international sanctions list.
4. You agree to provide information if required by applicable law.
5. You understand that suspicious transactions may be reported to authorities.

This service complies with international AML/KYC standards and reserves the right to refuse service at its discretion.
"""


def aml_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ I agree", callback_data="aml_accept")],
        [InlineKeyboardButton(text="❌ I decline", callback_data="aml_decline")],
    ])


async def check_aml(callback: CallbackQuery, state: FSMContext) -> bool:
    """
    Check if user has accepted AML. If not — show AML screen and return False.
    Call this at the start of action_swap and action_fiat.
    Returns True if user can proceed, False if AML screen was shown.
    """
    from database.db import has_accepted_aml
    user_id = callback.from_user.id
    if await has_accepted_aml(user_id):
        return True

    lang = await get_user_lang(user_id)
    await callback.message.edit_text(
        AML_TEXT,
        reply_markup=aml_keyboard(lang)
    )
    # Store what the user was trying to do so we can resume after AML
    data = await state.get_data()
    pending = "swap" if callback.data == "action_swap" else "fiat"
    await state.update_data(aml_pending=pending)
    return False


@router.callback_query(F.data == "aml_accept")
async def cb_aml_accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    await accept_aml(user_id)

    lang    = await get_user_lang(user_id)
    data    = await state.get_data()
    pending = data.get("aml_pending", "swap")

    await callback.message.edit_text(
        "✅ <b>Agreement accepted.</b>\n\nYou can now use the service.",
    )

    # Resume what the user was doing
    if pending == "fiat":
        from keyboards.inline import fiat_keyboard
        await callback.message.answer(
            "💳 <b>Buy crypto with card</b>\n\nChoose your payment currency:",
            reply_markup=await fiat_keyboard(lang)
        )
        from aiogram.fsm.state import State
        from states import ExchangeStates
        await state.set_state(ExchangeStates.waiting_currency_from)
        await state.update_data(is_fiat=True)
    else:
        from keyboards.inline import crypto_from_keyboard
        await callback.message.answer(
            "🔄 <b>New swap</b>\n\nChoose the currency you want to <b>send</b>:",
            reply_markup=await crypto_from_keyboard(lang)
        )
        from states import ExchangeStates
        await state.set_state(ExchangeStates.waiting_currency_from)
        await state.update_data(is_fiat=False)


@router.callback_query(F.data == "aml_decline")
async def cb_aml_decline(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    lang = await get_user_lang(callback.from_user.id)
    from keyboards.inline import main_menu
    await callback.message.edit_text(
        "❌ You declined the AML agreement.\n\n"
        "You cannot use the exchange service without accepting the policy.",
        reply_markup=main_menu(lang)
    )