# Generated by Django 4.2.4 on 2023-08-21 23:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_room_host_room_topic_alter_room_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={"ordering": ["-updated", "-created"]},
        ),
    ]
