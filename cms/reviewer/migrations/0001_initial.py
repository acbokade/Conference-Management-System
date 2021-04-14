# Generated by Django 3.1.2 on 2021-04-14 11:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gsp', '0001_initial'),
        ('accounts', '0001_initial'),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prior_reviewing_experience', models.CharField(max_length=250)),
                ('prior_research_paper_submissions', models.PositiveIntegerField()),
                ('area_expertise', models.CharField(max_length=250)),
                ('paper_review_limit', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3)])),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True)),
                ('novelty', models.TextField(blank=True)),
                ('impact', models.TextField(blank=True)),
                ('strong_points', models.TextField(blank=True)),
                ('weak_points', models.TextField(blank=True)),
                ('paper_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsp.papersubmission')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.reviewer')),
            ],
        ),
    ]
