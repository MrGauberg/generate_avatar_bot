# Generated by Django 4.2.16 on 2025-02-15 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("packages", "0002_packagetype_payment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="package",
            options={"verbose_name": "Пакет", "verbose_name_plural": "Пакеты"},
        ),
        migrations.AlterModelOptions(
            name="packagetype",
            options={
                "verbose_name": "Тип пакета",
                "verbose_name_plural": "Типы пакетов",
            },
        ),
        migrations.AlterModelOptions(
            name="payment",
            options={
                "verbose_name": "Платеж Юкасса",
                "verbose_name_plural": "Платежи Юкасса",
            },
        ),
        migrations.AddField(
            model_name="package",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="package",
            name="name",
            field=models.CharField(default="Базовый", max_length=40),
        ),
        migrations.AlterField(
            model_name="packagetype",
            name="name",
            field=models.CharField(max_length=40),
        ),
    ]
