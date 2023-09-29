from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
    )

author = 'Geoffrey Castillo'

doc = """
Generic outro for all experiments.
"""


class Constants(BaseConstants):
    name_in_url = 'outro'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comments = models.LongStringField(
        label='Do you have any comments that would help us to improve our study? This is completely optional.',
        blank=True
        )
