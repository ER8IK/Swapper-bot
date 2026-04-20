from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.currencies import CRYPTO_CURRENCIES, FIAT_CURRENCIES

def main_menu(lang: str = "en") -> InlineKeyboardMarkup:
    from services.i18n import t
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_swap"), callback_data="action_swap")],
        [InlineKeyboardButton(text=t(lang, "btn_buy_card"), callback_data="action_fiat")],
        [InlineKeyboardButton(text=t(lang, "btn_how"), callback_data="action_how")],
        [InlineKeyboardButton(text=t(lang, "btn_language"), callback_data="action_language")],
    ])

def back_to_menu(lang: str = "en") -> InlineKeyboardMarkup:
    from services.i18n import t
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="action_back")]
    ])

def cancel_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    from services.i18n import t
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="action_cancel")]
    ])

def crypto_from_keyboard(exclude_ticker: str = None, exclude_network: str = None) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for c in CRYPTO_CURRENCIES:
        if c["ticker"] == exclude_ticker and c["network"] == exclude_network:
            continue
        row.append(InlineKeyboardButton(text=c["label"], callback_data=f"from_{c['ticker']}_{c['network']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="action_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def crypto_to_keyboard(exclude_ticker: str = None, exclude_network: str = None) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for c in CRYPTO_CURRENCIES:
        if c["ticker"] == exclude_ticker and c["network"] == exclude_network:
            continue
        row.append(InlineKeyboardButton(text=c["label"], callback_data=f"to_{c['ticker']}_{c['network']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="action_cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def fiat_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for c in FIAT_CURRENCIES:
        buttons.append([InlineKeyboardButton(text=c["label"], callback_data=f"fiat_{c['ticker']}_{c['network']}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="action_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_keyboard(lang: str = "en", is_fiat: bool = False) -> InlineKeyboardMarkup:
    from services.i18n import t
    # Разделяем callback_data, чтобы хэндлеры не конфликтовали
    cb_yes = "fiat_confirm_yes" if is_fiat else "confirm_yes"
    cb_no = "fiat_confirm_no" if is_fiat else "confirm_no"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "btn_confirm"), callback_data=cb_yes),
            InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data=cb_no),
        ]
    ])