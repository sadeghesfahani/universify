# Generated by Django 3.2.6 on 2021-09-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_lend_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lend',
            name='end_date',
            field=models.DateField(),
        ),
    ]
