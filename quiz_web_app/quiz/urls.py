from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizListView.as_view(), name='index'),
    path('quiz/<int:pk>/', login_required(views.QuizDetailView.as_view()), name='quiz-detail'),
    path('question/<int:pk>/', login_required(views.QuestionDetailView.as_view()), name='question-detail'),
    path('result/<int:pk>/', login_required(views.ResultDetailView.as_view()), name='result-detail'),
    path('start-quiz/<int:pk>/', views.quiz_start, name='quiz-start'),
    path('user-submits-answer/', views.user_submits_answer, name='user-submits-answer'),
    path('drop-result/<int:pk>', views.drop_result_view, name='drop-result'),
]
