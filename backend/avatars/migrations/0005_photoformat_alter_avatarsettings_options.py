# Generated by Django 4.2.16 on 2025-02-16 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("avatars", "0004_avatarsettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="PhotoFormat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("format", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "Формат фото",
                "verbose_name_plural": "Форматы фото",
            },
        ),
        migrations.AlterModelOptions(
            name="avatarsettings",
            options={
                "verbose_name": "Настройки аватара",
                "verbose_name_plural": "Настройки аватаров",
            },
        ),
    ]
