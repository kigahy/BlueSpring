# Generated by Django 4.2.11 on 2024-11-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PolicyUpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('value', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='YouthPolicy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
