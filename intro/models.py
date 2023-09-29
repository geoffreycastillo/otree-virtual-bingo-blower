from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    )

author = 'Geoffrey Castillo'

doc = """
Generic intro app for Prolific
"""


class Constants(BaseConstants):
    name_in_url = 'intro'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    # uncommented in production
    # used to not forget to change the completion code
    # def creating_session(self):
    # if self.session.config['completion_code'] == 'TO CHANGE':
            #     raise ValueError('Please change the completion code')
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    browser_name = models.StringField()
    browser_version = models.StringField()
    device = models.StringField()
    os_name = models.StringField()
    os_version = models.StringField()
    fps = models.FloatField()
