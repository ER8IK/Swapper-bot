from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import ExchangeStates
from services import simpleswap
from services.currencies import get_currency, get_min_amount
from services.limiter import limiter
from database.db import save_swap
from keyboards.inline import (
    back_to_menu, cancel_keyboard, confirm_keyboard,
    fiat_keyboard, crypto_to_keyboard
)
import logging

logger = logging.getLogger(__name__)
router = Router()

ADDRESS_MIN_LENGTH = {"btc": 25, "eth": 42, "usdt": 42, "sol": 32, "bnb": 42, "trx": 34}

@router.callback_query(F.data == "action_fiat")
async def start_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    allowed, reason = limiter.check(callback.from_user.id)
    if not allowed:
        await callback.message.edit_text(reason, reply_markup=back_to_menu())
        return

    await state.set_state(ExchangeStates.waiting_currency_from)
    await state.update_data(is_fiat=True)
    await callback.message.edit_text(
        "💳 <b>Buy crypto with card</b>\n\nChoose your payment currency:",
        reply_markup=fiat_keyboard()
    )

@router.callback_query(ExchangeStates.waiting_currency_from, F.data.startswith("fiat_"))
async def choose_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    currency = get_currency(parts[1], parts[2])
    if not currency: return

    await state.update_data(currency_from=parts[1], network_from=parts[2], label_from=currency["label"])
    await state.set_state(ExchangeStates.waiting_currency_to)
    await callback.message.edit_text(
        f"✅ Paying with: <b>{currency['label']}</b>\n\nChoose crypto to receive:",
        reply_markup=crypto_to_keyboard()
    )

@router.callback_query(ExchangeStates.waiting_currency_to, F.data.startswith("to_"))
async def choose_crypto_for_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    if not data.get("is_fiat"): return

    parts = callback.data.split("_")
    currency = get_currency(parts[1], parts[2])
    if not currency: return

    await state.update_data(currency_to=parts[1], network_to=parts[2], label_to=currency["label"])
    await state.set_state(ExchangeStates.waiting_amount)
    min_amt = get_min_amount(data["currency_from"], data["network_from"])

    await callback.message.edit_text(
        f"✅ Receiving: <b>{currency['label']}</b>\n\nEnter amount in <b>{data['label_from']}</b>:\n"
        f"<i>Minimum: {min_amt} {data['currency_from'].upper()}</i>",
        reply_markup=cancel_keyboard()
    )

@router.message(ExchangeStates.waiting_amount)
async def enter_fiat_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("is_fiat"): return

    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0: raise ValueError
    except ValueError:
        await message.answer("⚠️ Enter valid amount.", reply_markup=cancel_keyboard())
        return

    await state.update_data(amount=amount)
    msg = await message.answer("⏳ Fetching quote...")
    est = await simpleswap.get_estimated(data["currency_from"], data["network_from"], data["currency_to"], data["network_to"], str(amount))

    if not est:
        await msg.edit_text("❌ Could not get a quote.", reply_markup=cancel_keyboard())
        return

    await state.update_data(amount_to=est["estimatedAmountTo"])
    await state.set_state(ExchangeStates.waiting_address)
    await msg.edit_text(
        f"💱 <b>Quote:</b>\n\nYou pay: <b>{amount} {data['label_from']}</b>\n"
        f"You receive: <b>≈{est['estimatedAmountTo']} {data['label_to']}</b>\n\nEnter wallet address:",
        reply_markup=cancel_keyboard()
    )

@router.message(ExchangeStates.waiting_address)
async def enter_fiat_address(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("is_fiat"): return

    address = message.text.strip()
    await state.update_data(address_to=address)
    await state.set_state(ExchangeStates.confirm)

    await message.answer(
        f"📋 <b>Confirm purchase:</b>\n\nYou pay: <b>{data['amount']} {data['label_from']}</b>\n"
        f"You receive: <b>≈{data['amount_to']} {data['label_to']}</b>\n"
        f"Address: <code>{address}</code>",
        reply_markup=confirm_keyboard(is_fiat=True) # <--- ТУТ ТЕПЕРЬ True
    )

@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_yes")
async def confirm_fiat_exchange(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text("⏳ Creating order...")

    result = await simpleswap.create_exchange(
        data["currency_from"], data["network_from"], data["currency_to"], data["network_to"],
        str(data["amount"]), data["address_to"]
    )

    if not result:
        await callback.message.edit_text("❌ Failed.", reply_markup=back_to_menu())
        return

    ex_id = result.get("id") or result.get("exchangeId")
    url = result.get("redirectUrl") or result.get("paymentUrl")

    await save_swap(callback.from_user.id, ex_id, f"{data['currency_from']}_{data['network_from']}", 
                    f"{data['currency_to']}_{data['network_to']}", data["amount"], data["amount_to"], data["address_to"])
    
    await state.clear()
    text = f"✅ <b>Order created!</b>\n\nID: <code>{ex_id}</code>\n"
    if url: text += f"\n👉 <a href='{url}'><b>PAY WITH CARD HERE</b></a>\n"
    
    await callback.message.edit_text(text, reply_markup=back_to_menu(), disable_web_page_preview=True)

@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_no")
async def cancel_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer(); await state.clear()
    await callback.message.edit_text("❌ Cancelled.", reply_markup=back_to_menu())