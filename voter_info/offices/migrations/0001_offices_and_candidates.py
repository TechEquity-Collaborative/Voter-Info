# Generated by Django 2.0.4 on 2018-06-16 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('districts', '0003_null_district_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('incumbent', models.BooleanField(default=False)),
                ('url', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='districts.District')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offices.Office'),
        ),
        migrations.AlterUniqueTogether(
            name='office',
            unique_together={('name', 'district')},
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('name', 'office')},
        ),
    ]