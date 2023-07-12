# Generated by Django 4.1.9 on 2023-06-23 08:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_rename_comment_commentofpost_rename_like_likeofpost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentofpost",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="imagesofpost",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="likeofpost",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]