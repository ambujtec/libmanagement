# Generated by Django 5.0.4 on 2024-04-07 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_borrowedbook_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=100)),
                ('book_name', models.CharField(max_length=100)),
                ('borrowed_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('renewed', models.BooleanField(default=False)),
            ],
        ),
    ]