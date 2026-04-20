from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states import ExchangeStates
from services import simpleswap
from services.currencies import get_currency, get_min_amount
from services.limiter import limiter
from database.db import save_swap
from keyboards.inline import back_to_menu, cancel_keyboard, fiat_keyboard, crypto_to_keyboard

router = Router()

# Функция для создания клавиатуры подтверждения (внутри файла для надежности)
def get_fiat_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="fiat_confirm_yes"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="fiat_confirm_no")
        ]
    ])

# ... (начальные хэндлеры выбора валют и суммы остаются как были) ...

@router.message(ExchangeStates.waiting_address)
async def enter_fiat_address(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("is_fiat"): return

    address = message.text.strip()
    await state.update_data(address_to=address)
    await state.set_state(ExchangeStates.confirm)

    await message.answer(
        f"📋 <b>Confirm Fiat Purchase:</b>\n\n"
        f"Pay: <b>{data['amount']} {data['label_from']}</b>\n"
        f"Receive: <b>≈{data['amount_to']} {data['label_to']}</b>\n"
        f"Wallet: <code>{address}</code>",
        reply_markup=get_fiat_confirm_kb() # Используем уникальные callback_data
    )

@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_yes")
async def confirm_fiat_exchange(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text("⏳ Creating secure payment link...")

    # ВАЖНО: убедись, что функция create_exchange в simpleswap.py 
    # умеет принимать параметры для фиата
    result = await simpleswap.create_exchange(
        ticker_from=data["currency_from"],
        network_from=data["network_from"],
        ticker_to=data["currency_to"],
        network_to=data["network_to"],
        amount=str(data["amount"]),
        address_to=data["address_to"]
    )

    if not result:
        # Если API вернуло ошибку, выводим её в консоль для отладки
        print(f"DEBUG: API Error result is empty") 
        await callback.message.edit_text(
            "❌ SimpleSwap API Error.\nCheck if the amount is within limits or your API key supports Fiat.",
            reply_markup=back_to_menu()
        )
        return

    ex_id = result.get("id") or result.get("exchangeId")
    # Ищем ссылку на оплату в разных возможных полях
    pay_url = result.get("redirectUrl") or result.get("paymentUrl") or result.get("redirect_url")

    await save_swap(
        user_id=callback.from_user.id,
        exchange_id=ex_id,
        currency_from=f"{data['currency_from']}_{data['network_from']}",
        currency_to=f"{data['currency_to']}_{data['network_to']}",
        amount_from=data["amount"],
        amount_to=data["amount_to"],
        address_to=data["address_to"]
    )

    await state.clear()

    if pay_url:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 GO TO PAYMENT PAGE", url=pay_url)],
            [InlineKeyboardButton(text="🏠 Main Menu", callback_data="action_back")]
        ])
        await callback.message.edit_text(
            f"✅ <b>Order {ex_id} created!</b>\n\n"
            "To complete the purchase with your card, click the button below. "
            "You will be redirected to a secure payment provider.",
            reply_markup=markup
        )
    else:
        # Если ссылки нет, значит это создался обычный крипто-своп по ошибке
        addr_from = result.get("addressFrom")
        await callback.message.edit_text(
            f"✅ Order created, but no card link found.\n"
            f"Send funds to: <code>{addr_from}</code>",
            reply_markup=back_to_menu()
        )

@router.callback_query(ExchangeStates.confirm, F.data == "fiat_confirm_no")
async def cancel_fiat(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("❌ Cancelled.", reply_markup=back_to_menu())