# Generated by Django 3.1.6 on 2021-04-15 12:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conference', '0001_initial'),
        ('gsp', '0001_initial'),
        ('accounts', '0001_initial'),
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
        migrations.CreateModel(
            name='InvitedReviewers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
