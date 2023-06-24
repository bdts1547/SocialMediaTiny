# Generated by Django 4.1.9 on 2023-06-24 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_imagesofpost_post_alter_profile_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentofpost",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="core.post",
            ),
        ),
        migrations.AlterField(
            model_name="likeofpost",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="core.post",
            ),
        ),
    ]
