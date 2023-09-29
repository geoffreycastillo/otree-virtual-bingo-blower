import itertools
import json
import random
from base64 import b64encode
from itertools import cycle

from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c
    )

import utils

author = 'Geoffrey Castillo'

doc = """
Your app description
"""

BALLS_PROPORTIONS = [6, 15, 9]

TREATMENTS = {
    'dow': {
        'event': 'dow'
        },
    'blower-10': {
        'event': 'blower',
        'number_balls': [2, 5, 3],
        'show_proportions': False
        },
    'blower-60': {
        'event': 'blower',
        'number_balls': [i * 2 for i in BALLS_PROPORTIONS],
        'show_proportions': False
        },
    'blower-30-ambiguity': {
        'event': 'blower',
        'number_balls': BALLS_PROPORTIONS,
        'show_proportions': False
        },
    'blower-60-ambiguity': {
        'event': 'blower',
        'number_balls': [i * 2 for i in BALLS_PROPORTIONS],
        'show_proportions': False
        },
    'blower-60-risk': {
        'event': 'blower',
        'number_balls': [i * 2 for i in BALLS_PROPORTIONS],
        'show_proportions': True
        }
    }


def encode_balls(ball_list):
    return b64encode(json.dumps(ball_list).encode('ascii')).decode('utf-8')


class Constants(BaseConstants):
    name_in_url = 'measure_ambiguity'
    players_per_group = None

    # define css colours and find human-readable colour names
    robot_colour_states = ('Red', 'MediumSlateBlue', 'Gold')
    human_colour_states = [None] * len(robot_colour_states)
    for index, colour in enumerate(robot_colour_states):
        human_colour_states[index] = utils.find_human_colour(colour).lower()

    DOW_states = [
        'decreases by more than 0.51%',
        'decreases by less than 0.51% or increases by less than 0.11%',
        'increases by more than 0.11%'
        ]

    number_single_events = len(robot_colour_states)
    states = list(itertools.product([True, False], repeat=number_single_events))
    # remove (False, False, False) and (True, True, True)
    states = [state for state in states if state not in [(False, False, False), (True, True, True)]]

    number_states = len(states)
    num_rounds = number_states

    payoff = c(3)


class Subsession(BaseSubsession):

    def initialise_treatment(self, player, treatments):
        player.participant.vars['treatment'] = next(treatments)
        player.participant.vars['event'] = TREATMENTS[player.participant.vars['treatment']]['event']
        if player.participant.vars['event'] == 'blower':
            player.participant.vars['number_balls'] = TREATMENTS[player.participant.vars['treatment']]['number_balls']
            player.participant.vars['show_proportions'] = TREATMENTS[player.participant.vars['treatment']]['show_proportions']
            player.participant.vars['percentage_balls'] = [num_ball / sum(player.participant.vars['number_balls']) * 100 for num_ball in
                                                           player.participant.vars['number_balls']]

    def creating_session(self):

        if self.round_number == 1:
            treatments = cycle(self.session.config['treatments'])

        for player in self.get_players():
            if self.round_number == 1:
                # initialise everything
                self.initialise_treatment(player, treatments)

                player.participant.vars['states'] = Constants.states.copy()
                random.shuffle(player.participant.vars['states'])

            player.treatment = player.participant.vars['treatment']

            player.states = json.dumps(Constants.human_colour_states if player.participant.vars['event'] == 'blower' else Constants.DOW_states)
            state = player.participant.vars['states'][self.round_number - 1]
            player.state = json.dumps(state)

            is_composite = state.count(True) != 1
            if is_composite:
                probabilities = [0, 20] + [35 + step for step in range(0, 60, 5)] + [93, 95, 97, 98, 99, 100]
            else:
                probabilities = [0, 1, 2, 5] + [10 + step for step in range(0, 70, 5)] + [85, 100]

            player.probabilities = json.dumps(probabilities)

            # payment
            if self.round_number == Constants.num_rounds:
                player.question_to_pay = random.randint(1, Constants.num_rounds)
                player.line_to_pay = random.randint(1, len(probabilities))
                player.payment_draw = random.randint(0, 100)


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def determine_display(self, player=None):
        state = json.loads(self.state if player is None else player.state)
        probabilities = json.loads(self.probabilities if player is None else player.probabilities)

        to_return = {
            'probabilities': probabilities,
            'state': state,
            }

        if self.participant.vars['event'] == 'blower':
            proportions = [[num_ball, colour, percentage] for num_ball, colour, percentage in
                           zip(self.participant.vars['number_balls'], Constants.human_colour_states, self.participant.vars['percentage_balls'])]
            number_balls = encode_balls(self.participant.vars['number_balls'])

            to_return = {
                **to_return,
                'proportions': proportions,
                'number_balls': number_balls
                }

        return to_return

    def find_switch_probability(self, choices, probabilities):
        choices = choices.split(",")
        switching_points_indexes = []

        # check if choices are well-behaved and if yes extract the valuation
        if (choices[0] == "A") & (choices[-1] == "B"):
            # the choice at the top is A and the one at the bottom is a B
            # so potentially we have a switching point
            # we can start looping to find it
            # note: we start from the bottom
            for index, value in enumerate(choices):
                if value == "B":
                    if choices[index - 1] != value:
                        switching_points_indexes.append(index)
            if not switching_points_indexes:
                probability = -2
            elif len(switching_points_indexes) == 1:
                probability = (probabilities[switching_points_indexes[0]] + probabilities[switching_points_indexes[0] - 1]) / 2
            else:
                probability = -3
        else:
            probability = -1

        return probability

    def determine_payment(self):
        player_in_round_to_pay = self.in_round(self.question_to_pay)

        payment_display = self.determine_display(player_in_round_to_pay)
        self.participant.vars['state'] = payment_display['state']

        line_to_pay = self.line_to_pay
        choice_at_line_to_pay = player_in_round_to_pay.choices.split(',')[line_to_pay - 1]

        self.payment_type = payment_type = 'lottery' if choice_at_line_to_pay == 'B' else ('blower' if self.participant.vars['event'] == 'blower' else 'DOW')

        payment_info = {
            **payment_display,
            'choice_at_line_to_pay': choice_at_line_to_pay,
            'payment_type': payment_type
            }

        if payment_type == 'lottery':
            draw = self.payment_draw
            win_cutoff = payment_display['probabilities'][line_to_pay - 1]
            win = True if draw < win_cutoff else False
            self.payoff = Constants.payoff if win else 0

            payment_info = {
                **payment_info,
                'draw': draw,
                'win_cutoff': win_cutoff,
                'win': win
                }

        elif payment_type == 'DOW':
            payment_state = []
            state = payment_display['state']
            for i, value in enumerate(state):
                if value:
                    payment_state.append(Constants.DOW_states[i])
            self.payment_state = json.dumps(payment_state)

        return payment_info

    def live_colour_drawn(self, data):
        self.payment_state = data

    # treatments
    treatment = models.StringField()

    states = models.StringField()
    state = models.StringField()
    probabilities = models.StringField()
    choices = models.StringField()
    switch_probability = models.FloatField()

    question_to_pay = models.IntegerField()
    line_to_pay = models.IntegerField()
    payment_type = models.StringField()
    payment_draw = models.IntegerField()
    payment_state = models.StringField()


def custom_export(players):
    yield ['time_started', 'id_in_session', 'participant code', 'Prolific ID',
           'treatment', 'current_app_name', 'current_page_name',
           'payoff',
           'payment_type', 'payment_draw', 'payment_state',
           'DOW_date',
           'bulk_bonus_command']

    for player in players:
        participant = player.participant
        if player.round_number == Constants.num_rounds \
                and participant._current_app_name == player.session.config['app_sequence'][-1] \
                and participant._current_page_name == 'End' \
                and participant.label is not None \
                and (participant.payoff > player.session.config['participation_fee'] or player.payment_type == 'DOW'):
            yield [participant.time_started, participant.id_in_session, participant.code, participant.label,
                   player.treatment, participant._current_app_name, participant._current_page_name,
                   participant.payoff,
                   player.payment_type, player.payment_draw, player.payment_state,
                   player.session.config['DOW_date'],
                   f'{participant.label}, {int(participant.payoff)}']
