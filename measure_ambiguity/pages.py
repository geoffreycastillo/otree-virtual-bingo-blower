import json
from .models import Constants

from ._builtin import Page


class Task(Page):
    form_model = 'player'
    form_fields = ['choices']

    def vars_for_template(self):
        display = self.player.determine_display()
        return display

    def before_next_page(self):
        self.player.switch_probability = self.player.find_switch_probability(self.player.choices, json.loads(self.player.probabilities))


class EndPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Results(EndPage):
    # form_model = 'player'
    live_method = 'live_colour_drawn'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return self.player.determine_payment()

    def before_next_page(self):
        if self.player.payment_type == 'blower':
            self.player.payoff = Constants.payoff \
                if self.player.payment_state in [state * colour for state, colour in zip(self.player.participant.vars['state'], Constants.human_colour_states)] \
                else 0


class PayoffDisplay(EndPage):
    ...


page_sequence = [Task, Results, PayoffDisplay]
