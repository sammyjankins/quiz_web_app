# Generated by Django 4.1.3 on 2022-12-15 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_result_right_result_wrong'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='wrong',
            new_name='answers',
        ),
    ]