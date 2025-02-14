FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

COPY ../requirements.txt .
RUN sleep 5 && pip install --no-cache-dir -r requirements.txt --index-url=https://pypi.org/simple/

COPY . .
