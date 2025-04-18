# Generated by Django 4.2.16 on 2025-02-13 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("packages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackageType",
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
                ("name", models.CharField(max_length=20)),
                ("total_generations", models.IntegerField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                (
                    "payment_id",
                    models.CharField(
                        help_text="ID платежа в ЮKassa", max_length=100, unique=True
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, help_text="Сумма платежа", max_digits=10
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидание"),
                            ("succeeded", "Успешно"),
                            ("canceled", "Отменен"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name="package",
            old_name="used_generations",
            new_name="generations_remains",
        ),
        migrations.RemoveField(
            model_name="package",
            name="total_generations",
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.AddField(
            model_name="payment",
            name="package",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="packages.package",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="package",
            name="package_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="packages.packagetype"
            ),
        ),
    ]
