# Generated by Django 4.2 on 2023-04-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0002_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="quiz_id",
            field=models.CharField(max_length=100, null=True),
        ),
    ]