# Generated by Django 3.1.6 on 2021-04-20 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('gsp', '0001_initial'),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaChair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conference.conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='AssignedAreaChairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_chair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area_chair.areachair')),
                ('paper_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsp.papersubmission')),
            ],
        ),
        migrations.CreateModel(
            name='AreaChairDecision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_review', models.TextField(blank=True)),
                ('decision', models.TextField(blank=True)),
                ('area_chair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area_chair.areachair')),
                ('paper_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsp.papersubmission')),
            ],
        ),
    ]
