from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from states import ExchangeStates
from services import simpleswap
from services.currencies import get_fiat_currencies, get_crypto_currencies, get_currency, get_min_amount
from services.limiter import limiter
from database.db import save_swap
from keyboards.inline import (
    back_to_menu, cancel_keyboard, fiat_confirm_keyboard,
    fiat_keyboard, crypto_to_keyboard
)

import logging

logger = logging.getLogger(__name__)
router = Router()

ADDRESS_MIN_LENGTH = {
    "btc": 25, "eth": 42, "usdt": 42,
    "sol": 32, "bnb": 42, "trx": 34,
}


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
    ticker = parts[1]
    network = parts[2]
    currency = get_currency(ticker, network)
    if not currency:
        await callback.answer("Unknown currency", show_alert=True)
        return

    await state.update_data(
        currency_from=ticker,
        network_from=network,
        label_from=currency["label"]
    )
    await state.set_state(ExchangeStates.waiting_currency_to)
    await callback.message.edit_text(
        f"✅ Paying with: <b>{currency['label']}</b>\n\nChoose crypto to receive:",
        reply_markup=crypto_to_keyboard()
    )


@router.callback_query(ExchangeStates.waiting_currency_to, F.data.startswith("to_"))
async def choose_crypto_for_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    if not data.get("is_fiat"):
        return  # не наш хендлер — пусть exchange.py обрабатывает

    parts = callback.data.split("_")
    ticker = parts[1]
    network = parts[2]
    currency = get_currency(ticker, network)
    if not currency:
        await callback.answer("Unknown currency", show_alert=True)
        return

    await state.update_data(
        currency_to=ticker,
        network_to=network,
        label_to=currency["label"]
    )
    await state.set_state(ExchangeStates.waiting_amount)
    min_amount = get_min_amount(data["currency_from"], data["network_from"])

    await callback.message.edit_text(
        f"✅ Receiving: <b>{currency['label']}</b>\n\n"
        f"Enter amount in <b>{data['label_from']}</b>:\n"
        f"<i>Minimum: {min_amount} {data['currency_from'].upper()}</i>\n\n"
        f"<i>Type /cancel to abort</i>",
        reply_markup=cancel_keyboard()
    )


@router.message(ExchangeStates.waiting_amount)
async def enter_fiat_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("is_fiat"):
        return

    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ Enter a valid amount, e.g. <b>100</b>\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    min_amount = get_min_amount(data["currency_from"], data["network_from"])
    if amount < min_amount:
        await message.answer(
            f"⚠️ Minimum amount: <b>{min_amount} {data['currency_from'].upper()}</b>\n\n"
            f"<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(amount=amount)
    msg = await message.answer("⏳ Fetching quote...")

    estimated_resp = await simpleswap.get_estimated(
        ticker_from=data["currency_from"],
        network_from=data["network_from"],
        ticker_to=data["currency_to"],
        network_to=data["network_to"],
        amount=str(amount)
    )

    if not estimated_resp:
        await msg.edit_text(
            f"❌ Could not get a quote.\n\n"
            f"Minimum: <b>{min_amount} {data['currency_from'].upper()}</b>\n"
            f"Try a higher amount.\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(amount_to=estimated_resp["estimatedAmountTo"])
    await state.set_state(ExchangeStates.waiting_address)

    await msg.edit_text(
        f"💱 <b>Quote:</b>\n\n"
        f"You pay: <b>{amount} {data['label_from']}</b>\n"
        f"You receive: <b>≈{estimated_resp['estimatedAmountTo']} {data['label_to']}</b>\n\n"
        f"Enter your <b>{data['label_to']}</b> wallet address:\n\n"
        f"<i>Type /cancel to abort</i>",
        reply_markup=cancel_keyboard()
    )


@router.message(ExchangeStates.waiting_address)
async def enter_fiat_address(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("is_fiat"):
        return

    address = message.text.strip()
    currency_to = data.get("currency_to", "")
    min_len = ADDRESS_MIN_LENGTH.get(currency_to, 10)

    if len(address) < min_len:
        await message.answer(
            f"⚠️ Address too short. Minimum {min_len} characters.\n"
            f"<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(address_to=address)
    await state.set_state(ExchangeStates.confirm)

    await message.answer(
        f"📋 <b>Confirm purchase:</b>\n\n"
        f"You pay: <b>{data['amount']} {data['label_from']}</b>\n"
        f"You receive: <b>≈{data['amount_to']} {data['label_to']}</b>\n"
        f"Address: <code>{address}</code>\n\n"
        f"Everything correct?",
        reply_markup=fiat_confirm_keyboard()
    )


# ---------------------------------------------------------------------------
# Подтверждение фиатного обмена — только fiat_confirm_yes
# ---------------------------------------------------------------------------

@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_yes")
async def confirm_fiat_exchange(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    if not data.get("is_fiat"):
        return

    await callback.message.edit_text("⏳ Creating order...")

    # ВАЖНО: Передаем аргументы явно. 
    # Если simpleswap.py ожидает другие имена полей, проверь их там.
    result = await simpleswap.create_exchange(
        ticker_from=data["currency_from"],
        network_from=data["network_from"],
        ticker_to=data["currency_to"],
        network_to=data["network_to"],
        amount=str(data["amount"]),
        address_to=data["address_to"]
    )

    if not result:
        logger.info(f"FIAT RESULT FULL: {result}")
        # Логируем в консоль бота, чтобы видеть реальную причину (например, API key error)
        logger.error(f"SimpleSwap Fiat Error for user {callback.from_user.id}: result is None")
        await callback.message.edit_text(
            "❌ Failed to create order. Your amount might be out of range or API is busy.\n"
            "Try again with a different amount.",
            reply_markup=back_to_menu()
        )
        await state.clear()
        return

    exchange_id = result.get("id") or result.get("exchangeId")
    # Проверяем все возможные варианты названия поля ссылки
    redirect_url = (
        result.get("redirectUrl") or 
        result.get("paymentUrl") or 
        result.get("redirect_url") or 
        result.get("payment_url")
    )

    await save_swap(
        user_id=callback.from_user.id,
        exchange_id=exchange_id,
        currency_from=f"{data['currency_from']}_{data['network_from']}",
        currency_to=f"{data['currency_to']}_{data['network_to']}",
        amount_from=data["amount"],
        amount_to=data["amount_to"],
        address_to=data["address_to"]
    )

    limiter.record(callback.from_user.id)
    await state.clear()

    if redirect_url:
        pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Pay now", url=redirect_url)],
            [InlineKeyboardButton(text="⬅️ Main menu", callback_data="action_back")],
        ])
        await callback.message.edit_text(
            f"✅ <b>Order created!</b>\n\n"
            f"ID: <code>{exchange_id}</code>\n"
            f"You will be redirected to the secure card payment page.\n\n"
            f"Check status: /status_{exchange_id}",
            reply_markup=pay_keyboard
        )
    else:
        # Ссылка не пришла — вероятно, API создал обычный крипто-своп
        address_from = result.get("addressFrom") or result.get("address_from")
        msg = f"✅ <b>Order created!</b>\n\nID: <code>{exchange_id}</code>\n"
        if address_from:
            msg += f"Send funds to: <code>{address_from}</code>"
        
        await callback.message.edit_text(msg, reply_markup=back_to_menu())


@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_no")
async def cancel_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("❌ Cancelled.", reply_markup=back_to_menu())