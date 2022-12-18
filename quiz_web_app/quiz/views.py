from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Quiz, Question, Result
from .services import start_or_continue_quiz, check_is_current, get_next_question, eval_user_selection, eval_result, \
    check_result_for_quiz, drop_result, get_progress


class QuizListView(ListView):
    model = Quiz
    template_name = "quiz/index.html"
    context_object_name = 'quizes'


class QuizDetailView(DetailView):
    model = Quiz

    def get_context_data(self, **kwargs):
        progress = get_progress(self.request.user, kwargs)
        kwargs.update({'progress': progress})
        return super(QuizDetailView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        result = check_result_for_quiz(request, kwargs)
        if result:
            return HttpResponseRedirect(reverse('result-detail', kwargs={'pk': result.pk}))
        return super(QuizDetailView, self).get(request, *args, **kwargs)


class QuestionDetailView(UserPassesTestMixin, DetailView):
    model = Question

    def test_func(self):
        return check_is_current(self)


class ResultDetailView(DetailView):
    model = Result


def quiz_start(request, **kwargs):
    question_pk = start_or_continue_quiz(request, kwargs)
    return HttpResponseRedirect(reverse('question-detail', kwargs={'pk': question_pk}))


def user_submits_answer(request, **kwargs):
    question, quiz = request.POST.getlist('quiz_detail[]')
    user_answered = eval_user_selection(request, question)
    if user_answered:
        question_pk = get_next_question(request.user, quiz)
        if question_pk:
            return HttpResponseRedirect(reverse('question-detail', kwargs={'pk': question_pk}))
        result = eval_result(request.user, quiz)
        return HttpResponseRedirect(reverse('result-detail', kwargs={'pk': result}))
    else:
        return HttpResponseRedirect(reverse('question-detail', kwargs={'pk': question}))


def drop_result_view(request, **kwargs):
    quiz_pk = drop_result(request, kwargs)
    return HttpResponseRedirect(reverse('quiz-detail', kwargs={'pk': quiz_pk}))
