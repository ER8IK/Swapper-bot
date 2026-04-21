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
        [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="action_back")]
    ])
    
# Добавь эту функцию в keyboards/inline.py

def fiat_confirm_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    from services.i18n import t
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "btn_confirm"), callback_data="fiat_confirm_yes"),
            InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="fiat_confirm_no"),
        ]
    ])


def crypto_from_keyboard(exclude_ticker: str = None,
                         exclude_network: str = None) -> InlineKeyboardMarkup:
    """Keyboard for selecting source crypto currency."""
    buttons = []
    row = []
    for c in CRYPTO_CURRENCIES:
        if c["ticker"] == exclude_ticker and c["network"] == exclude_network:
            continue
        row.append(InlineKeyboardButton(
            text=c["label"],
            callback_data=f"from_{c['ticker']}_{c['network']}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="action_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def crypto_to_keyboard(exclude_ticker: str = None,
                       exclude_network: str = None) -> InlineKeyboardMarkup:
    """Keyboard for selecting destination crypto currency."""
    buttons = []
    row = []
    for c in CRYPTO_CURRENCIES:
        if c["ticker"] == exclude_ticker and c["network"] == exclude_network:
            continue
        row.append(InlineKeyboardButton(
            text=c["label"],
            callback_data=f"to_{c['ticker']}_{c['network']}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="action_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def fiat_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting fiat currency."""
    buttons = []
    for c in FIAT_CURRENCIES:
        buttons.append([InlineKeyboardButton(
            text=c["label"],
            callback_data=f"fiat_{c['ticker']}_{c['network']}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="action_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    from services.i18n import t
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "btn_confirm"), callback_data="confirm_yes"),
            InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="confirm_no"),
        ]
    ])
