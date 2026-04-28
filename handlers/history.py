from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import back_to_menu
from database.db import get_user_swaps  

router = Router()

@router.callback_query(F.data == "action_history")
async def show_history(callback: CallbackQuery):
    await callback.answer()
    
    # Получаем последние 5-10 обменов пользователя
    swaps = await get_user_swaps(callback.from_user.id)
    
    if not swaps:
        await callback.message.edit_text(
            "📭 You haven't made any swaps yet.",
            reply_markup=back_to_menu()
        )
        return

    text = "📜 <b>Your Swap History:</b>\n\n"
    for s in swaps:
        # Эмодзи статуса
        status_icon = "⏳" if s['status'] == 'waiting' else "✅" if s['status'] == 'finished' else "❌"
        
        text += (
            f"{status_icon} <code>{s['exchange_id']}</code>\n"
            f"🔄 {s['currency_from'].upper()} ➡️ {s['currency_to'].upper()}\n"
            f"💰 {s['amount_from']} → {s['amount_to']}\n"
            f"📅 Status: <b>{s['status']}</b>\n"
            f"---------------------------\n"
        )

    await callback.message.edit_text(text, reply_markup=back_to_menu())