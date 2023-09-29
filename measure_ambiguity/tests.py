from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import json
from random import randint

class PlayerBot(Bot):
    def play_round(self):
        probabilities = json.loads(self.player.probabilities)
        length_probabilities = len(probabilities)
        switching_point = randint(0, length_probabilities - 1)
        choices = ['A' if n < switching_point else 'B' for n in range(length_probabilities)]
        choices = ",".join(choices)
        yield pages.Task, {'choices': choices}

        if self.round_number == Constants.num_rounds:
            yield pages.Results
            yield pages.PayoffDisplay
