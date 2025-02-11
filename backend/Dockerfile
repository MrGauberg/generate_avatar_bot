FROM python:3.9

# Установка рабочей директории
WORKDIR /app

# Обновление pip перед установкой зависимостей
RUN pip install --upgrade pip

# Принудительное ожидание сети перед установкой
COPY requirements.txt .
RUN sleep 5 && pip install --no-cache-dir -r requirements.txt --index-url=https://pypi.org/simple/

# Копирование остальных файлов проекта
COPY . .
