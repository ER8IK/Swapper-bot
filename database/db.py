import aiosqlite
import logging

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


async def update_swap_status(exchange_id: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE swaps SET status = ? WHERE exchange_id = ?",
            (status, exchange_id)
        )
        await db.commit()
        
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
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM swaps")
        total = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status = 'finished'"
        )
        finished = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status IN ('waiting', 'confirming', 'exchanging', 'sending')"
        )
        pending = (await cursor.fetchone())[0]

        cursor = await db.execute(
            "SELECT COUNT(*) FROM swaps WHERE status IN ('failed', 'expired')"
        )
        failed = (await cursor.fetchone())[0]

    return {
        "total": total,
        "finished": finished,
        "pending": pending,
        "failed": failed
    }