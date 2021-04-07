# Generated by Django 2.1 on 2021-04-07 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=250)),
                ('research_interests', models.CharField(max_length=500)),
                ('highest_degree', models.CharField(max_length=250)),
                ('google_scholar', models.CharField(max_length=250)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='accounts.User')),
            ],
        ),
    ]