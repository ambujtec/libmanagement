# Generated by Django 5.0.4 on 2024-04-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_borrowedbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='student',
            field=models.CharField(max_length=100),
        ),
    ]
