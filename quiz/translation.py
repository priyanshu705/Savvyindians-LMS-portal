from modeltranslation.translator import register, TranslationOptions
from .models import Quiz, Question, Choice, MCQuestion

@register(Quiz)
class QuizTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
    empty_values=None

"""
Note:
Temporarily disable translation registration for Question/MCQuestion.
On Python 3.13 with django-modeltranslation>=0.19 and
model_utils.InheritanceManager, manager patching can raise:
TypeError: __class__ assignment: 'NewMultilingualManager' object layout differs from 'InheritanceManager'
See issue discussion: modeltranslation tries to replace the model manager's
class, which conflicts with InheritanceManager used by Question.

If you switch to Python 3.10/3.11 with the project's pinned deps
(Django 4.0.x, modeltranslation 0.18.x), you can re-enable these
registrations safely.
"""

# @register(Question)
# class QuestionTranslationOptions(TranslationOptions):
#     fields = ('content', 'explanation',)
#     empty_values=None

@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('choice',)
    empty_values=None

# @register(MCQuestion)
# class MCQuestionTranslationOptions(TranslationOptions):
#     pass