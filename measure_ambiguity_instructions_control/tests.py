from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Instructions
        yield pages.Control, {
            'control_question_A_or_B_10': 'optionA',
            'control_question_if_A_10': 'gain20',
            'control_question_A_or_B_60': 'optionB',
            'control_question_if_B_60': 'lottery'
            }
