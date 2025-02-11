from __future__ import absolute_import, unicode_literals
import os
import subprocess

from celery import Celery

# Установка настроек Django для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.conf.broker_transport_options = {
    'visibility_timeout': 3600,
    'retry_on_timeout': True,
    'socket_keepalive': True,
    'max_connections': 100,
}

# Чтение конфигурации из Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическая регистрация задач из INSTALLED_APPS
app.autodiscover_tasks()



@app.task(name="check_redis_connection")
def check_redis_connection():
    try:
        app.broker_connection().ensure_connection()
    except ConnectionError:
        subprocess.run(["docker", "restart", "getcourse_celery_1"])