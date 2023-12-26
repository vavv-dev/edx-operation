# Generated by Django 4.2 on 2023-12-25 18:21

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OperationEvent",
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
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("event_type", models.CharField(db_index=True, max_length=255)),
                ("event_time", models.DateTimeField()),
                ("source_data", models.TextField()),
                ("success", models.BooleanField(blank=True, null=True)),
                ("error", models.TextField(blank=True, null=True)),
                ("retry_count", models.SmallIntegerField(default=0)),
            ],
            options={
                "verbose_name": "이벤트",
                "verbose_name_plural": "이벤트",
            },
        ),
    ]
