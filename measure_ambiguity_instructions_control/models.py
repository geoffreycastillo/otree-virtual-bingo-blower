from datetime import datetime
from itertools import cycle

from django.utils.safestring import mark_safe
from otree.api import (
    models,
    widgets,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c
    )

from measure_ambiguity import models as measure_ambiguity_models

author = 'Your name here'

doc = """
Your app description
"""


class Constants(measure_ambiguity_models.Constants):
    name_in_url = 'measure_ambiguity_instructions_control'
    players_per_group = None

    measure_ambiguity_num_rounds = measure_ambiguity_models.Constants.num_rounds
    num_rounds = 1

    state = (True, False, True)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            treatments = cycle(self.session.config['treatments'])

        for player in self.get_players():
            measure_ambiguity_models.Subsession.initialise_treatment(self, player, treatments)
            player.treatment = player.participant.vars['treatment']

        if 'DOW_date' in self.session.config and self.round_number == 1:
            date = datetime.strptime(self.session.config['DOW_date'], '%Y-%m-%d')
            self.session.vars['DOW_date'] = datetime.strftime(date, '%A %d %B %Y')

            # uncommented in production
            # used to not forget to change the date
            # if date < datetime.now():
            #     raise ValueError('The Dow date specified needs to be in the future!')


class Group(BaseGroup):
    pass


GAINS_CHOICES = [
    ['gain0', f'I gain {c(0)}'],
    ['gain20', f'I gain {measure_ambiguity_models.Constants.payoff}'],
    ['lottery', 'It is irrelevant: how much I gain depends on the random number selected by the computer to play Option B.'],
    ]


class Player(BasePlayer):
    treatment = models.StringField()

    control_question_A_or_B_10 = models.StringField(
        label=mark_safe(
            'Imagine that the line corresponding to a chance to win of 10% is selected. '
            'If your choices are as described in the example above, which option would you play at the end of the experiment?'),
        widget=widgets.RadioSelect,
        choices=[
            ['optionA', 'Option A'],
            ['optionB', 'Option B']
            ]
        )

    def control_question_A_or_B_10_error_message(self, value):
        if value != 'optionA':
            return mark_safe('This would be the case if on the line corresponding to a chance to win of 10% you had selected Option B.')

    control_question_if_A_10 = models.StringField(
        choices=GAINS_CHOICES,
        widget=widgets.RadioSelect,
        )

    def control_question_if_A_10_error_message(self, value):
        state = 'the ball drawn' if self.participant.vars['event'] == 'blower' else 'the evolution of the Dow'
        if value == 'lottery':
            return 'Remember that in this example and in this line you have chosen Option A, not Option B.'
        if value == 'gain0':
            return f'You gain {c(0)} if {state} is not displayed in Option A.'

    control_question_A_or_B_60 = models.StringField(
        label=mark_safe(
            'Imagine that the line corresponding to a chance to win of 60% is selected. '
            'If your choices are as described in the example above, which option would you play at the end of the experiment?'),
        widget=widgets.RadioSelect,
        choices=[
            ['optionA', 'Option A'],
            ['optionB', 'Option B']
            ]
        )

    def control_question_A_or_B_60_error_message(self, value):
        if value != 'optionB':
            return mark_safe('This would be the case if on the line corresponding to a chance to win of 60% you had selected Option A.')

    control_question_if_B_60 = models.StringField(
        choices=GAINS_CHOICES,
        widget=widgets.RadioSelect,
        )

    def control_question_if_B_60_error_message(self, value):
        if value != 'lottery':
            return f'You cannot be sure you will win {c(0)} or {c(20)}.'
