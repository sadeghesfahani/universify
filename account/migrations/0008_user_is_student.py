# Generated by Django 3.2.7 on 2021-09-01 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_rename_is_super_user_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]