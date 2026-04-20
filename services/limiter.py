import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# Лимиты
MAX_EXCHANGES_PER_HOUR = 3
MAX_EXCHANGES_PER_DAY = 10
WINDOW_HOUR = 3600   # 1 час в секундах
WINDOW_DAY = 86400   # 24 часа в секундах


class RateLimiter:
    def __init__(self):
        # user_id → список timestamps обменов
        self._timestamps: dict[int, list[float]] = defaultdict(list)

    def _clean(self, user_id: int):
        """Удалить устаревшие записи."""
        now = time.time()
        self._timestamps[user_id] = [
            t for t in self._timestamps[user_id]
            if now - t < WINDOW_DAY
        ]

    def check(self, user_id: int) -> tuple[bool, str]:
        """
        Проверить можно ли пользователю создать обмен.
        Возвращает (True, "") если можно,
        (False, причина) если нельзя.
        """
        self._clean(user_id)
        now = time.time()
        timestamps = self._timestamps[user_id]

        # Проверка часового лимита
        recent_hour = [t for t in timestamps if now - t < WINDOW_HOUR]
        if len(recent_hour) >= MAX_EXCHANGES_PER_HOUR:
            wait = int(WINDOW_HOUR - (now - min(recent_hour)))
            minutes = wait // 60
            seconds = wait % 60
            return False, (
                f"⏳ Слишком много обменов за последний час.\n\n"
                f"Максимум {MAX_EXCHANGES_PER_HOUR} обмена в час.\n"
                f"Попробуй через {minutes}м {seconds}с."
            )

        # Проверка дневного лимита
        if len(timestamps) >= MAX_EXCHANGES_PER_DAY:
            wait = int(WINDOW_DAY - (now - min(timestamps)))
            hours = wait // 3600
            minutes = (wait % 3600) // 60
            return False, (
                f"⏳ Достигнут дневной лимит обменов.\n\n"
                f"Максимум {MAX_EXCHANGES_PER_DAY} обменов в день.\n"
                f"Попробуй через {hours}ч {minutes}м."
            )

        return True, ""

    def record(self, user_id: int):
        """Записать факт создания обмена."""
        self._timestamps[user_id].append(time.time())
        logger.info(
            f"Rate limiter: user {user_id} — "
            f"{len(self._timestamps[user_id])} exchange(s) today"
        )


# Глобальный экземпляр — один на весь бот
limiter = RateLimiter()