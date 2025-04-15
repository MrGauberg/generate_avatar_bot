import logging
import os

# Создание логгера
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

# Формат логирования
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# Файловый обработчик (если нужна запись в файл)
log_file = os.getenv("LOG_FILE", "bot.log")
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

logger.info("Логирование настроено.")
