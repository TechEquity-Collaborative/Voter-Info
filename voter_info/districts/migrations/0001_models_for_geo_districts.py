# Generated by Django 2.0.4 on 2018-05-10 05:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shape_stle', models.FloatField(verbose_name='shape style')),
                ('dist_name', models.TextField(verbose_name='district name')),
                ('shape_star', models.FloatField(verbose_name='shape star')),
                ('district_i', models.FloatField(verbose_name='district ID')),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('shape_file_name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='districts.District'),
        ),
    ]
