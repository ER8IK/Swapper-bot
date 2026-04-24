from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import (
    get_all_swaps, get_stats, get_recent_logs,
    get_top_pairs, get_average_amount, get_volume_by_period,
    get_all_currencies_admin, add_currency,
    toggle_currency, update_currency_min, delete_currency
)
from config import ADMIN_ID
import logging

logger = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_add_ticker  = State()
    waiting_add_network = State()
    waiting_add_label   = State()
    waiting_add_min     = State()
    waiting_add_fiat    = State()
    waiting_edit_min    = State()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


def admin_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Manage currencies", callback_data="adm_currencies")],
        [InlineKeyboardButton(text="📋 Last swaps",        callback_data="adm_swaps")],
        [InlineKeyboardButton(text="📈 Top pairs",         callback_data="adm_pairs")],
        [InlineKeyboardButton(text="📋 Logs",              callback_data="adm_logs")],
    ])


# ── /admin ────────────────────────────────────────────────────────────────────

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    stats = await get_stats()
    avg   = await get_average_amount()

    await message.answer(
        f"👑 <b>Admin Panel</b>\n\n"
        f"📊 <b>Overall</b>\n"
        f"Total exchanges: <b>{stats['total']}</b>\n"
        f"Unique users: <b>{stats['users']}</b>\n"
        f"Avg amount: <b>{avg}</b>\n\n"
        f"📅 <b>By period</b>\n"
        f"Today: <b>{stats['today']}</b>\n"
        f"This week: <b>{stats['week']}</b>\n"
        f"This month: <b>{stats['month']}</b>\n\n"
        f"⚙️ <b>By status</b>\n"
        f"✅ Finished: <b>{stats['finished']}</b>\n"
        f"⏳ Pending: <b>{stats['pending']}</b>\n"
        f"❌ Failed: <b>{stats['failed']}</b>\n\n"
        f"📋 <b>Commands:</b>\n"
        f"/admin_currencies — manage currencies\n"
        f"/admin_swaps — last 10 exchanges\n"
        f"/admin_users — user list\n"
        f"/admin_pairs — top pairs\n"
        f"/admin_logs — recent logs",
        reply_markup=admin_main_keyboard()
    )


# ── Currency management ────────────────────────────────────────────────────────

async def _currencies_text_and_kb() -> tuple[str, InlineKeyboardMarkup]:
    currencies = await get_all_currencies_admin()

    if not currencies:
        text = "💰 <b>Currencies</b>\n\nNo currencies configured yet."
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Add currency", callback_data="adm_add_currency")],
            [InlineKeyboardButton(text="⬅️ Back",         callback_data="adm_back")],
        ])
        return text, kb

    lines = []
    for c in currencies:
        status = "✅" if c["is_active"] else "❌"
        ftype  = "FIAT" if c["is_fiat"] else "CRYPTO"
        lines.append(
            f"{status} <b>{c['label']}</b> — "
            f"<code>{c['ticker']}/{c['network']}</code> "
            f"[{ftype}] min: <b>{c['min_amount']}</b>"
        )
    text = "💰 <b>Currencies</b>\n\n" + "\n".join(lines)

    rows = []
    for c in currencies:
        toggle_txt = "🔴 Disable" if c["is_active"] else "🟢 Enable"
        rows.append([
            InlineKeyboardButton(text=c["label"],     callback_data=f"adm_cur_info_{c['id']}"),
            InlineKeyboardButton(text=toggle_txt,     callback_data=f"adm_cur_toggle_{c['id']}"),
            InlineKeyboardButton(text="✏️ Min",       callback_data=f"adm_cur_editmin_{c['id']}"),
            InlineKeyboardButton(text="🗑 Delete",    callback_data=f"adm_cur_delete_{c['id']}"),
        ])
    rows.append([InlineKeyboardButton(text="➕ Add currency", callback_data="adm_add_currency")])
    rows.append([InlineKeyboardButton(text="⬅️ Back",         callback_data="adm_back")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return text, kb


@router.message(Command("admin_currencies"))
async def cmd_admin_currencies(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return
    text, kb = await _currencies_text_and_kb()
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "adm_currencies")
async def cb_currencies(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    text, kb = await _currencies_text_and_kb()
    await callback.message.edit_text(text, reply_markup=kb)


# Toggle enable / disable
@router.callback_query(F.data.startswith("adm_cur_toggle_"))
async def cb_toggle(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    cur_id    = int(callback.data.split("_")[-1])
    new_state = await toggle_currency(cur_id)
    label     = "enabled ✅" if new_state else "disabled ❌"
    await callback.answer(f"Currency {label}", show_alert=True)
    text, kb  = await _currencies_text_and_kb()
    await callback.message.edit_text(text, reply_markup=kb)


# Edit minimum amount — step 1
@router.callback_query(F.data.startswith("adm_cur_editmin_"))
async def cb_editmin(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    cur_id = int(callback.data.split("_")[-1])
    await state.set_state(AdminStates.waiting_edit_min)
    await state.update_data(edit_currency_id=cur_id)
    await callback.message.edit_text(
        "✏️ <b>Edit minimum amount</b>\n\n"
        "Enter new minimum (e.g. <code>0.001</code>):\n\n"
        "<i>/cancel to abort</i>"
    )


@router.message(AdminStates.waiting_edit_min)
async def process_edit_min(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    try:
        new_min = float(message.text.replace(",", "."))
        if new_min < 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Invalid amount. Try again or /cancel")
        return
    data = await state.get_data()
    await update_currency_min(data["edit_currency_id"], new_min)
    await state.clear()
    await message.answer(f"✅ Minimum updated to <b>{new_min}</b>")
    text, kb = await _currencies_text_and_kb()
    await message.answer(text, reply_markup=kb)


# Delete — confirm step
@router.callback_query(F.data.startswith("adm_cur_delete_"))
async def cb_delete(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    cur_id = int(callback.data.split("_")[-1])
    await callback.message.edit_text(
        "🗑 <b>Confirm deletion?</b>\n\nThis cannot be undone.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Yes, delete",
                    callback_data=f"adm_cur_confirmdelete_{cur_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="adm_currencies"
                ),
            ]
        ])
    )


@router.callback_query(F.data.startswith("adm_cur_confirmdelete_"))
async def cb_confirm_delete(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    cur_id = int(callback.data.split("_")[-1])
    await delete_currency(cur_id)
    await callback.answer("🗑 Deleted", show_alert=True)
    text, kb = await _currencies_text_and_kb()
    await callback.message.edit_text(text, reply_markup=kb)


# Add currency — 5-step dialog
@router.callback_query(F.data == "adm_add_currency")
async def cb_add_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    await state.set_state(AdminStates.waiting_add_ticker)
    await callback.message.edit_text(
        "➕ <b>Add currency — Step 1/5</b>\n\n"
        "Enter the <b>ticker</b>\n"
        "Example: <code>btc</code>, <code>eth</code>, <code>matic</code>\n\n"
        "<i>/cancel to abort</i>"
    )


@router.message(AdminStates.waiting_add_ticker)
async def process_add_ticker(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(new_ticker=message.text.strip().lower())
    await state.set_state(AdminStates.waiting_add_network)
    await message.answer(
        "➕ <b>Step 2/5</b>\n\n"
        "Enter the <b>network</b>\n"
        "Example: <code>eth</code>, <code>bsc</code>, <code>trx</code>, <code>sol</code>\n"
        "For fiat use same as ticker: <code>usd</code>, <code>eur</code>\n\n"
        "<i>/cancel to abort</i>"
    )


@router.message(AdminStates.waiting_add_network)
async def process_add_network(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(new_network=message.text.strip().lower())
    await state.set_state(AdminStates.waiting_add_label)
    await message.answer(
        "➕ <b>Step 3/5</b>\n\n"
        "Enter the <b>display label</b> shown to users\n"
        "Example: <code>MATIC</code>, <code>USDT (TRC20)</code>\n\n"
        "<i>/cancel to abort</i>"
    )


@router.message(AdminStates.waiting_add_label)
async def process_add_label(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(new_label=message.text.strip())
    await state.set_state(AdminStates.waiting_add_min)
    await message.answer(
        "➕ <b>Step 4/5</b>\n\n"
        "Enter the <b>minimum amount</b>\n"
        "Example: <code>5.0</code>\n\n"
        "<i>/cancel to abort</i>"
    )


@router.message(AdminStates.waiting_add_min)
async def process_add_min(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    try:
        min_amount = float(message.text.replace(",", "."))
        if min_amount < 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Invalid amount. Try again or /cancel")
        return
    await state.update_data(new_min=min_amount)
    await state.set_state(AdminStates.waiting_add_fiat)
    await message.answer(
        "➕ <b>Step 5/5</b>\n\n"
        "Is this a <b>fiat</b> currency (USD, EUR)?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Yes — fiat",  callback_data="adm_add_fiat_yes"),
                InlineKeyboardButton(text="🔗 No — crypto", callback_data="adm_add_fiat_no"),
            ]
        ])
    )


@router.callback_query(F.data.startswith("adm_add_fiat_"))
async def process_add_fiat(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    is_fiat = callback.data == "adm_add_fiat_yes"
    data    = await state.get_data()
    await state.clear()

    cur_id = await add_currency(
        ticker     = data["new_ticker"],
        network    = data["new_network"],
        label      = data["new_label"],
        min_amount = data["new_min"],
        is_fiat    = is_fiat,
    )

    ftype = "fiat" if is_fiat else "crypto"
    await callback.message.edit_text(
        f"✅ <b>Currency added!</b>\n\n"
        f"Label: <b>{data['new_label']}</b>\n"
        f"Ticker: <code>{data['new_ticker']}</code>\n"
        f"Network: <code>{data['new_network']}</code>\n"
        f"Min: <b>{data['new_min']}</b>\n"
        f"Type: <b>{ftype}</b>\n"
        f"ID: <code>{cur_id}</code>"
    )
    text, kb = await _currencies_text_and_kb()
    await callback.message.answer(text, reply_markup=kb)


# ── Back to admin main ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "adm_back")
async def cb_adm_back(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    stats = await get_stats()
    avg   = await get_average_amount()
    await callback.message.edit_text(
        f"👑 <b>Admin Panel</b>\n\n"
        f"📊 Total: <b>{stats['total']}</b>  |  Users: <b>{stats['users']}</b>  |  Avg: <b>{avg}</b>\n\n"
        f"📅 Today: <b>{stats['today']}</b>  |  Week: <b>{stats['week']}</b>  |  Month: <b>{stats['month']}</b>\n\n"
        f"✅ Finished: <b>{stats['finished']}</b>  "
        f"⏳ Pending: <b>{stats['pending']}</b>  "
        f"❌ Failed: <b>{stats['failed']}</b>",
        reply_markup=admin_main_keyboard()
    )


# ── Swaps ──────────────────────────────────────────────────────────────────────

@router.message(Command("admin_swaps"))
async def cmd_admin_swaps(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return
    swaps = await get_all_swaps(limit=10)
    if not swaps:
        await message.answer("📭 No exchanges yet.")
        return
    text = "📋 <b>Last exchanges:</b>\n\n"
    for s in swaps:
        text += (
            f"👤 <code>{s['user_id']}</code> | "
            f"{s['amount_from']} {s['currency_from'].upper()} → "
            f"{s['currency_to'].upper()} | {s['status']}\n"
            f"   <code>{s['exchange_id']}</code>\n\n"
        )
    await message.answer(text)


@router.callback_query(F.data == "adm_swaps")
async def cb_adm_swaps(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    swaps = await get_all_swaps(limit=10)
    if not swaps:
        await callback.message.edit_text("📭 No exchanges yet.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Back", callback_data="adm_back")]
            ]))
        return
    text = "📋 <b>Last exchanges:</b>\n\n"
    for s in swaps:
        text += (
            f"👤 <code>{s['user_id']}</code> | "
            f"{s['amount_from']} {s['currency_from'].upper()} → "
            f"{s['currency_to'].upper()} | {s['status']}\n"
            f"   <code>{s['exchange_id']}</code>\n\n"
        )
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back", callback_data="adm_back")]
    ]))


# ── Pairs ──────────────────────────────────────────────────────────────────────

@router.message(Command("admin_pairs"))
async def cmd_admin_pairs(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return
    pairs = await get_top_pairs()
    if not pairs:
        await message.answer("📭 No finished exchanges yet.")
        return
    medals = ["🥇", "🥈", "🥉", "4.", "5."]
    text   = "📈 <b>Top pairs:</b>\n\n"
    for i, p in enumerate(pairs):
        m = medals[i] if i < len(medals) else f"{i+1}."
        text += (
            f"{m} <b>{p['currency_from'].upper()} → {p['currency_to'].upper()}</b>\n"
            f"   Exchanges: {p['count']} | Volume: {round(p['volume'], 4)}\n\n"
        )
    await message.answer(text)


@router.callback_query(F.data == "adm_pairs")
async def cb_adm_pairs(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    pairs = await get_top_pairs()
    if not pairs:
        await callback.message.edit_text("📭 No finished exchanges yet.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Back", callback_data="adm_back")]
            ]))
        return
    medals = ["🥇", "🥈", "🥉", "4.", "5."]
    text   = "📈 <b>Top pairs:</b>\n\n"
    for i, p in enumerate(pairs):
        m = medals[i] if i < len(medals) else f"{i+1}."
        text += (
            f"{m} <b>{p['currency_from'].upper()} → {p['currency_to'].upper()}</b>\n"
            f"   Exchanges: {p['count']} | Volume: {round(p['volume'], 4)}\n\n"
        )
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back", callback_data="adm_back")]
    ]))


# ── Users ──────────────────────────────────────────────────────────────────────

@router.message(Command("admin_users"))
async def cmd_admin_users(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return
    swaps = await get_all_swaps(limit=200)
    users: dict = {}
    for s in swaps:
        uid = s["user_id"]
        users[uid] = users.get(uid, 0) + 1
    if not users:
        await message.answer("📭 No users yet.")
        return
    text = f"👥 <b>Users ({len(users)}):</b>\n\n"
    for uid, cnt in sorted(users.items(), key=lambda x: -x[1]):
        text += f"<code>{uid}</code> — {cnt} exchange(s)\n"
    await message.answer(text)


# ── Logs ───────────────────────────────────────────────────────────────────────

@router.message(Command("admin_logs"))
async def cmd_admin_logs(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return
    lines = await get_recent_logs(20)
    if not lines:
        await message.answer("📭 No logs yet.")
        return
    text = "\n".join(lines)
    for chunk in [text[i:i+3500] for i in range(0, len(text), 3500)]:
        await message.answer(f"📋 <b>Recent logs:</b>\n\n<pre>{chunk}</pre>")


@router.callback_query(F.data == "adm_logs")
async def cb_adm_logs(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    lines = await get_recent_logs(20)
    text  = "\n".join(lines) if lines else "No logs yet."
    chunk = text[:3500]
    await callback.message.edit_text(
        f"<pre>{chunk}</pre>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back", callback_data="adm_back")]
        ])
    )