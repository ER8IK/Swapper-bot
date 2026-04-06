from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
import re

from states import ExchangeStates
from services import simpleswap
from database.db import save_swap
from keyboards.inline import back_to_menu, cancel_keyboard

import logging

logger = logging.getLogger(__name__)
router = Router()

POPULAR_COINS = ["btc", "eth", "usdt", "sol", "bnb", "trx"]

ADDRESS_MIN_LENGTH = {
    "btc": 25, "eth": 42, "usdt": 42,
    "sol": 32, "bnb": 42, "trx": 34,
}


# ---------------------------------------------------------------------------
# Keyboards
# ---------------------------------------------------------------------------

def coins_keyboard(exclude: str = None) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for coin in POPULAR_COINS:
        if coin == exclude:
            continue
        row.append(InlineKeyboardButton(
            text=coin.upper(),
            callback_data=f"coin_{coin}"
        ))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="action_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="confirm_no"),
        ]
    ])


# ---------------------------------------------------------------------------
# /cancel command — works at any step
# ---------------------------------------------------------------------------

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await message.answer("No active action. Type /start")
        return
    await state.clear()
    await message.answer("❌ Cancelled.\n\nType /start to begin again.")


# ---------------------------------------------------------------------------
# Cancel via inline button — works at any step
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "action_cancel")
async def callback_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    try:
        await callback.message.edit_text(
            "❌ Cancelled.\n\nType /start to begin again."
        )
    except TelegramBadRequest:
        pass


# ---------------------------------------------------------------------------
# Step 1 — Start swap, choose currency FROM
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "action_swap")
async def start_swap(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ExchangeStates.waiting_currency_from)
    try:
        await callback.message.edit_text(
            "🔄 <b>New swap</b>\n\nChoose the currency you want to <b>send</b>:",
            reply_markup=coins_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


# ---------------------------------------------------------------------------
# Step 2 — Choose currency TO
# ---------------------------------------------------------------------------

@router.callback_query(ExchangeStates.waiting_currency_from, F.data.startswith("coin_"))
async def choose_from(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    coin = callback.data.split("_")[1]
    await state.update_data(currency_from=coin)
    await state.set_state(ExchangeStates.waiting_currency_to)
    await callback.message.edit_text(
        f"✅ Sending: <b>{coin.upper()}</b>\n\n"
        f"Now choose the currency you want to <b>receive</b>:",
        reply_markup=coins_keyboard(exclude=coin)
    )


# ---------------------------------------------------------------------------
# Step 3 — Enter amount
# ---------------------------------------------------------------------------

@router.callback_query(ExchangeStates.waiting_currency_to, F.data.startswith("coin_"))
async def choose_to(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    coin = callback.data.split("_")[1]
    await state.update_data(currency_to=coin)
    await state.set_state(ExchangeStates.waiting_amount)
    data = await state.get_data()
    await callback.message.edit_text(
        f"✅ Receiving: <b>{coin.upper()}</b>\n\n"
        f"Enter the amount in <b>{data['currency_from'].upper()}</b>:\n\n"
        f"<i>Type /cancel to abort</i>",
        reply_markup=cancel_keyboard()
    )


@router.message(ExchangeStates.waiting_amount)
async def enter_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ Enter a valid amount, e.g. <b>0.01</b>\n\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    data = await state.get_data()
    await state.update_data(amount=amount)

    msg = await message.answer("⏳ Fetching quote...")

    estimated_resp = await simpleswap.get_estimated(
        ticker_from=data["currency_from"],
        ticker_to=data["currency_to"],
        amount=str(amount)
    )

    if not estimated_resp:
        await msg.edit_text(
            "❌ <b>Could not get a quote.</b>\n\n"
            "Possible reasons:\n"
            "• Amount is too small\n"
            "• Pair is temporarily unavailable\n"
            "• API issue\n\n"
            "Try a different amount or pair.\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return  # keep state — let user try another amount

    await state.update_data(amount_to=estimated_resp["estimatedAmountTo"])
    await state.set_state(ExchangeStates.waiting_address)

    await msg.edit_text(
        f"💱 <b>Quote:</b>\n\n"
        f"You send: <b>{amount} {data['currency_from'].upper()}</b>\n"
        f"You receive: <b>≈{estimated_resp['estimatedAmountTo']} {data['currency_to'].upper()}</b>\n\n"
        f"Enter the destination wallet address for <b>{data['currency_to'].upper()}</b>:\n\n"
        f"<i>Type /cancel to abort</i>",
        reply_markup=cancel_keyboard()
    )


# ---------------------------------------------------------------------------
# Step 4 — Enter destination address
# ---------------------------------------------------------------------------

@router.message(ExchangeStates.waiting_address)
async def enter_address(message: Message, state: FSMContext):
    address = message.text.strip()
    data = await state.get_data()
    currency_to = data.get("currency_to", "")
    min_len = ADDRESS_MIN_LENGTH.get(currency_to, 10)

    if len(address) < min_len:
        await message.answer(
            f"⚠️ Address too short for <b>{currency_to.upper()}</b>.\n"
            f"Minimum {min_len} characters, you entered {len(address)}.\n\n"
            f"Check the address and try again.\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    if not re.match(r'^[a-zA-Z0-9]+$', address):
        await message.answer(
            "⚠️ Address contains invalid characters.\n"
            "Check and try again.\n<i>Type /cancel to abort</i>",
            reply_markup=cancel_keyboard()
        )
        return

    await state.update_data(address_to=address)
    await state.set_state(ExchangeStates.confirm)

    await message.answer(
        f"📋 <b>Confirm swap:</b>\n\n"
        f"You send: <b>{data['amount']} {data['currency_from'].upper()}</b>\n"
        f"You receive: <b>≈{data['amount_to']} {data['currency_to'].upper()}</b>\n"
        f"Address: <code>{address}</code>\n\n"
        f"Everything correct?",
        reply_markup=confirm_keyboard()
    )


# ---------------------------------------------------------------------------
# Step 5 — Confirm or cancel
# ---------------------------------------------------------------------------

@router.callback_query(ExchangeStates.confirm, F.data == "confirm_yes")
async def confirm_exchange(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text("⏳ Creating exchange...")

    result = await simpleswap.create_exchange(
        ticker_from=data["currency_from"],
        ticker_to=data["currency_to"],
        amount=str(data["amount"]),
        address_to=data["address_to"]
    )

    if not result:
        await callback.message.edit_text(
            "❌ Failed to create exchange. Please try again later.",
            reply_markup=back_to_menu()
        )
        await state.clear()
        return

    exchange_id = result.get("id") or result.get("exchangeId")
    address_from = result.get("addressFrom") or result.get("address_from")

    await save_swap(
        user_id=callback.from_user.id,
        exchange_id=exchange_id,
        currency_from=data["currency_from"],
        currency_to=data["currency_to"],
        amount_from=data["amount"],
        amount_to=data["amount_to"],
        address_to=data["address_to"]
    )

    await state.clear()
    await callback.message.edit_text(
        f"✅ <b>Exchange created!</b>\n\n"
        f"ID: <code>{exchange_id}</code>\n"
        f"Send <b>{data['amount']} {data['currency_from'].upper()}</b> to:\n"
        f"<code>{address_from}</code>\n\n"
        f"Check status: /status_{exchange_id}",
        reply_markup=back_to_menu()
    )


@router.callback_query(ExchangeStates.confirm, F.data == "confirm_no")
async def cancel_exchange(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        "❌ Exchange cancelled.",
        reply_markup=back_to_menu()
    )