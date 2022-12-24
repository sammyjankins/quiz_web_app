from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all()

    def user_current_quiz(self):
        current_questions = UserQuestion.objects.filter(quiz=self.id, status=UserQuestion.status_opt[2])
        if current_questions:
            return [question.user for question in current_questions]
        else:
            return None

    def user_has_results(self):
        results = Result.objects.filter(quiz=self.id)
        if results:
            return [result.user for result in results]
        else:
            return None

    class Meta:
        verbose_name_plural = 'Quizes'


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answers.all()

    def is_only_correct(self):
        correctness = [answer.correct for answer in self.get_answers()]
        return correctness.count(True) == 1


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    answers = models.IntegerField(default=None)
    right = models.IntegerField(default=None)

    def __str__(self):
        return f'Результат: {self.score}'


class UserQuestion(models.Model):
    status_opt = (
        ('unanswered', "Unanswered"),
        ('answered', "Answered"),
        ('current', "Current"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    status = models.CharField(choices=status_opt, max_length=50)


class UserAnswer(models.Model):
    status_opt = (
        ('incorrect', "Incorrect"),
        ('correct', "Correct"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_question = models.ForeignKey(UserQuestion, on_delete=models.CASCADE, default=None, related_name='user_answers')
    status = models.CharField(choices=status_opt, max_length=50)
