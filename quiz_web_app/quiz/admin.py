from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from nested_admin.nested import NestedInlineModelAdmin, NestedTabularInline, NestedModelAdmin, NestedStackedInline

from .models import Quiz, Question, Answer, Result, UserAnswer, UserQuestion


class AnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        empty_forms = 0
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['correct']:
                    count += 1
            else:
                empty_forms += 1
        if count == 0:
            raise ValidationError('Должен быть указан как минимум один правильный ответ на вопрос.')

        if count == len(self.forms) - empty_forms:
            raise ValidationError('Все ответы не могут быть правильными.')


class AnswerInline(NestedInlineModelAdmin, NestedTabularInline):
    model = Answer
    formset = AnswerInlineFormset

    def get_extra(self, request, obj=None, **kwargs):
        return 2


class QuestionAdmin(NestedModelAdmin):
    inlines = (AnswerInline,)


class QuestionInline(NestedInlineModelAdmin, NestedStackedInline):
    model = Question
    inlines = (AnswerInline,)

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class QuizAdmin(NestedModelAdmin):
    inlines = (QuestionInline,)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Result)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserAnswer)
admin.site.register(UserQuestion)
