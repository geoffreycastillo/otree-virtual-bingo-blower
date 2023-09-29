from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Feedback(Page):
    form_model = 'player'
    form_fields = ['comments']


class End(Page):
    pass


page_sequence = [Feedback, End]
