# Generated by Django 3.1.6 on 2021-04-13 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_researchprofile'),
        ('reviewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True)),
                ('novelty', models.TextField(blank=True)),
                ('impact', models.TextField(blank=True)),
                ('strong_points', models.TextField(blank=True)),
                ('weak_points', models.TextField(blank=True)),
                ('paper_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.reviewer')),
            ],
        ),
    ]
