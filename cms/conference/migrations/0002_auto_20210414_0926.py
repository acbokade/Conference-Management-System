# Generated by Django 3.1.6 on 2021-04-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='workshop',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]