# Generated by Django 4.1.3 on 2022-12-15 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_remove_useranswer_question_remove_useranswer_quiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='user_question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quiz.userquestion'),
        ),
    ]
