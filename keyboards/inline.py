from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Swap", callback_data="action_swap"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ How it works", callback_data="action_how"),
        ]
    ])


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Back", callback_data="action_back"),
        ]
    ])


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Cancel", callback_data="action_cancel"),
        ]
    ])