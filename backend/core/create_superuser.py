import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def create_super_user():
    from users.models import CustomUser
    from dotenv import load_dotenv

    load_dotenv()

    EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD", "password")

    if not CustomUser.objects.filter(email=EMAIL).exists():
        CustomUser.objects.create_superuser(EMAIL, PASSWORD)


create_super_user()
