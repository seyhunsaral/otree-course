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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'jsoutput'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cc_0 = models.IntegerField(min=0, max=5, label="0")
    cc_1 = models.IntegerField(min=0, max=5, label="1")
    cc_2 = models.IntegerField(min=0, max=5, label="2")
    cc_3 = models.IntegerField(min=0, max=5, label="3")
    cc_4 = models.IntegerField(min=0, max=5, label="4")
    cc_5 = models.IntegerField(min=0, max=5, label="5")

    contribution = models.IntegerField()
