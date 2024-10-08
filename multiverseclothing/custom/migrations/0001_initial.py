# Generated by Django 5.0.7 on 2024-08-01 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TShirtColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='designs/')),
                ('tshirt_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom.tshirtcolor')),
            ],
        ),
    ]
