import aiosqlite
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
DB_PATH = "swaps.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS swaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exchange_id TEXT,
                currency_from TEXT,
                currency_to TEXT,
                amount_from REAL,
                amount_to REAL,
                address_to TEXT,
                status TEXT DEFAULT 'created',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    logger.info("Database initialized")


async def save_swap(user_id: int, exchange_id: str, currency_from: str,
                    currency_to: str, amount_from: float, amount_to: float,
                    address_to: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO swaps (user_id, exchange_id, currency_from, currency_to,
                               amount_from, amount_to, address_to)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, exchange_id, currency_from, currency_to,
              amount_from, amount_to, address_to))
        await db.commit()
        return cursor.lastrowid


async def get_user_swaps(user_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM swaps WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
async def get_top_pairs(limit: int = 5) -> list:
    """Top trading pairs by volume."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT
                currency_from,
                currency_to,
                COUNT(*) as count,
                SUM(amount_from) as volume
            FROM swaps
            WHERE status = 'finished'
            GROUP BY currency_from, currency_to
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]



async def update_swap_status(exchange_id: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE swaps SET status = ? WHERE exchange_id = ?",
            (status, exchange_id)
        )
        await db.commit()
        
async def get_average_amount() -> float:
    """Average exchange amount."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT AVG(amount_from) FROM swaps WHERE status = 'finished'"
        )
        result = (await cursor.fetchone())[0]
        return round(result, 6) if result else 0.0
    
async def get_volume_by_period(days: int) -> dict:
    """Exchange count and unique users for a given period."""
    async with aiosqlite.connect(DB_PATH) as db:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor = await db.execute("""
            SELECT
                COUNT(*) as count,
                COUNT(DISTINCT user_id) as users
            FROM swaps
            WHERE DATE(created_at) >= ? AND status = 'finished'
        """, (since,))
        row = await cursor.fetchone()
        return {"count": row[0], "users": row[1]}
        
async def get_all_swaps(limit: int = 10) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM swaps ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_stats() -> dict:
    """General stats for admin panel."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Всего
        cursor = await db.execute("SELECT COUNT(*) FROM swaps")
        total = (await cursor.fetchone())[0]

        # По статусам
        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status = 'finished'"
        )
        finished = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status IN "
            "('waiting', 'confirming', 'exchanging', 'sending')"
        )
        pending = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status IN ('failed', 'expired')"
        )
        failed = (await cursor.fetchone())[0]

        # Уникальные пользователи
        cursor = await db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM swaps"
        )
        users = (await cursor.fetchone())[0]

        # За сегодня
        today = datetime.now().strftime("%Y-%m-%d")
        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE DATE(created_at) = ?", (today,)
        )
        today_count = (await cursor.fetchone())[0]

        # За неделю
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE DATE(created_at) >= ?", (week_ago,)
        )
        week_count = (await cursor.fetchone())[0]

        # За месяц
        month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE DATE(created_at) >= ?", (month_ago,)
        )
        month_count = (await cursor.fetchone())[0]

        return {
            "total": total,
            "finished": finished,
            "pending": pending,
            "failed": failed,
            "users": users,
            "today": today_count,
            "week": week_count,
            "month": month_count,
        }
    
async def get_active_swaps() -> list:
    """Get all swaps that are not in a final state."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM swaps
            WHERE status NOT IN ('finished', 'failed', 'refunded', 'expired')
            AND exchange_id IS NOT NULL
            ORDER BY created_at DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
async def get_recent_logs(n: int = 20) -> list[str]:
    """Read last N lines from bot.log."""
    log_path = os.path.join("logs", "bot.log")
    if not os.path.exists(log_path):
        return ["Log file not found."]
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [l.strip() for l in lines[-n:] if l.strip()]
    except Exception as e:
        return [f"Error reading logs: {e}"]