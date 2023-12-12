# Generated by Django 4.2.7 on 2023-12-03 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False, help_text='Designate if the user has Owner status', verbose_name='Owner Status'),
        ),
    ]