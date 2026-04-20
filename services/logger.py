import logging
import logging.handlers
import os

LOG_DIR = "logs"
BOT_LOG = os.path.join(LOG_DIR, "bot.log")
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")


def setup_logging():
    """Configure logging with file rotation."""
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Корневой логгер
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Консоль
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)

    # bot.log — всё (ротация 5MB, хранить 5 файлов)
    bot_file = logging.handlers.RotatingFileHandler(
        BOT_LOG,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    bot_file.setFormatter(formatter)
    bot_file.setLevel(logging.INFO)

    # errors.log — только ошибки
    error_file = logging.handlers.RotatingFileHandler(
        ERROR_LOG,
        maxBytes=2 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    error_file.setFormatter(formatter)
    error_file.setLevel(logging.ERROR)

    root.addHandler(console)
    root.addHandler(bot_file)
    root.addHandler(error_file)