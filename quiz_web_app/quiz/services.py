from .models import UserAnswer, Quiz, Question, Answer, UserQuestion, Result


def get_next_question(user, quiz):
    current = UserQuestion.objects.filter(user=user, quiz=quiz, status=UserQuestion.status_opt[2]).first()
    if current:
        return current.question.pk
    else:
        unanswered = UserQuestion.objects.filter(user=user, quiz=quiz, status=UserQuestion.status_opt[0]).first()
        if unanswered:
            unanswered.status = UserQuestion.status_opt[2]
            unanswered.save()
            return unanswered.question.pk
        return None


def start_or_continue_quiz(request, kwargs):
    quiz = Quiz.objects.get(pk=kwargs['pk'])
    check_current = UserQuestion.objects.filter(user=request.user, quiz=quiz, status=UserQuestion.status_opt[2])
    if not check_current:
        question_list = Question.objects.filter(quiz=quiz)
        for question in question_list:
            UserQuestion.objects.create(user=request.user, quiz=quiz,
                                        question=question, status=UserQuestion.status_opt[0])
    return get_next_question(request.user, quiz)


def check_is_current(instance):
    item = instance.get_object()
    current = UserQuestion.objects.filter(user=instance.request.user,
                                          quiz=item.quiz, status=UserQuestion.status_opt[2]).first()
    return item == current.question


def eval_user_selection(request, question):
    user_question = UserQuestion.objects.filter(user=request.user, question=question).first()
    user_selection_list = [answer.split('_')[1] for answer in request.POST if answer.startswith('answer')]
    if user_selection_list:
        for user_selection in user_selection_list:
            answer = Answer.objects.get(id=user_selection)
            UserAnswer.objects.create(user=request.user,
                                      user_question=user_question,
                                      status=UserAnswer.status_opt[int(answer.correct)])
        user_question.status = UserQuestion.status_opt[1]
        user_question.save()
        return True
    return False


def eval_result(user, quiz):
    answers = 0
    right = 0
    for user_question in UserQuestion.objects.filter(user=user, quiz=quiz):
        for user_answer in user_question.user_answers.all():
            answers += 1
            if ''.join(filter(str.isalpha, user_answer.status.split(',')[0])) == 'correct':
                right += 1
    score = (right / answers) * 100
    quiz = Quiz.objects.get(pk=quiz)
    result = Result.objects.create(user=user, quiz=quiz, answers=answers, right=right, score=score)
    return result.pk


def check_result_for_quiz(request, kwargs):
    result = Result.objects.filter(quiz=kwargs['pk'], user=request.user)
    if len(result):
        return result.first()
    else:
        return None


def drop_result(request, kwargs):
    result = Result.objects.get(pk=kwargs['pk'])
    quiz = result.quiz
    quiz_user_questions = UserQuestion.objects.filter(user=request.user, quiz=result.quiz)
    for question in quiz_user_questions:
        question.user_answers.all().delete()
    quiz_user_questions.delete()
    result.delete()
    return quiz.pk


def get_progress(user, kwargs):
    quiz = kwargs['object']
    questions = quiz.question_set.count()
    user_answered = UserQuestion.objects.filter(quiz=quiz, user=user, status=UserQuestion.status_opt[1]).count()
    return (user_answered / questions) * 100
