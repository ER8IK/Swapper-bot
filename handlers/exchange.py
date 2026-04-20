from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states import ExchangeStates
from services import simpleswap
from services.currencies import get_currency, get_min_amount
from services.limiter import limiter
from database.db import save_swap
from keyboards.inline import (
    back_to_menu, cancel_keyboard, confirm_keyboard,
    crypto_from_keyboard, crypto_to_keyboard
)
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear(); await message.answer("❌ Cancelled.")

@router.callback_query(F.data == "action_swap")
async def start_swap(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ExchangeStates.waiting_currency_from)
    await state.update_data(is_fiat=False)
    await callback.message.edit_text("🔄 <b>New swap</b>\n\nChoose currency to send:", reply_markup=crypto_from_keyboard())

@router.callback_query(ExchangeStates.waiting_currency_from, F.data.startswith("from_"))
async def choose_from(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    currency = get_currency(parts[1], parts[2])
    await state.update_data(currency_from=parts[1], network_from=parts[2], label_from=currency["label"])
    await state.set_state(ExchangeStates.waiting_currency_to)
    await callback.message.edit_text(f"✅ Sending: {currency['label']}", reply_markup=crypto_to_keyboard(exclude_ticker=parts[1]))

@router.callback_query(ExchangeStates.waiting_currency_to, F.data.startswith("to_"))
async def choose_to(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    currency = get_currency(parts[1], parts[2])
    data = await state.get_data()
    if data.get("is_fiat"): return # Даем работать buywithcard.py
    
    await state.update_data(currency_to=parts[1], network_to=parts[2], label_to=currency["label"])
    await state.set_state(ExchangeStates.waiting_amount)
    min_amt = get_min_amount(data["currency_from"], data["network_from"])
    await callback.message.edit_text(f"✅ Receiving: {currency['label']}\nMin: {min_amt}", reply_markup=cancel_keyboard())

@router.message(ExchangeStates.waiting_amount)
async def enter_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("is_fiat"): return
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        est = await simpleswap.get_estimated(data["currency_from"], data["network_from"], data["currency_to"], data["network_to"], str(amount))
        await state.update_data(amount_to=est["estimatedAmountTo"])
        await state.set_state(ExchangeStates.waiting_address)
        await message.answer(f"Quote: {est['estimatedAmountTo']} {data['currency_to']}\nEnter address:", reply_markup=cancel_keyboard())
    except: await message.answer("Error. Try again.")

@router.message(ExchangeStates.waiting_address)
async def enter_address(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("is_fiat"): return
    address = message.text.strip()
    await state.update_data(address_to=address)
    await state.set_state(ExchangeStates.confirm)
    await message.answer(f"📋 <b>Confirm swap:</b>\n{data['amount']} -> {data['amount_to']}\nAddr: {address}", 
                         reply_markup=confirm_keyboard(is_fiat=False))

@router.callback_query(ExchangeStates.confirm, F.data == "confirm_yes")
async def confirm_exchange(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get("is_fiat"): return # ИГНОРИРУЕМ ФИАТ

    await callback.answer()
    await callback.message.edit_text("⏳ Creating exchange...")
    result = await simpleswap.create_exchange(data["currency_from"], data["network_from"], data["currency_to"], data["network_to"], str(data["amount"]), data["address_to"])
    
    if result:
        addr_from = result.get("addressFrom")
        await callback.message.edit_text(f"✅ Created! Send funds to:\n<code>{addr_from}</code>", reply_markup=back_to_menu())
    await state.clear()

@router.callback_query(ExchangeStates.confirm, F.data == "confirm_no")
async def cancel_exchange(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get("is_fiat"): return
    await callback.answer(); await state.clear()
    await callback.message.edit_text("❌ Cancelled.", reply_markup=back_to_menu())