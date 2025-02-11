# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ../bot /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Определяем переменные окружения (можно передавать через .env)
ENV BOT_TOKEN=""
ENV API_URL=""

# Запускаем бота
CMD ["python", "main.py"]
