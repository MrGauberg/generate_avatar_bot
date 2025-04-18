# Generated by Django 4.2.16 on 2025-03-04 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("avatars", "0009_avatar_is_complete"),
        ("prompts", "0003_alter_promptstyle_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="promptstyle",
            name="gender",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="avatars.avatargender",
            ),
        ),
        migrations.AddField(
            model_name="promptstyle",
            name="prompt",
            field=models.TextField(default=""),
        ),
    ]
