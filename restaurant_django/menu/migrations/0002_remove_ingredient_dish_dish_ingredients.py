# Generated by Django 5.1.3 on 2024-11-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='dish',
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(related_name='dishes', to='menu.ingredient'),
        ),
    ]