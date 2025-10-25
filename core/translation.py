from modeltranslation.translator import TranslationOptions, register

from .models import NewsAndEvents


@register(NewsAndEvents)
class NewsAndEventsTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "summary",
    )
    empty_values = None
