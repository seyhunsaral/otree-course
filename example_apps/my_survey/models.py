import random
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
    name_in_url = 'my_survey'
    players_per_group = 3
    num_rounds = 1
    safe_amount = 3
    risky_amount = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.StringField(label = "Please tell me your name")
    risk_att1 = models.IntegerField(label = "How old are you?", min=18, max=117)
    risk_att2 = models.BooleanField(label = "Are you a student?", blank = True)
    punishment_given = models.StringField(choices=[["MAT","Mathemathics"],["LAW","Law"]], widget=widgets.RadioSelect())

    risky_selected = models.BooleanField(choices = [[True, "Option A"],[False, "Option B"]])

    def set_payoffs(self):
        if self.risky_selected:
            self.payoff = random.choice([0,Constants.risky_amount])
        else:
            self.payoff = c(Constants.safe_amount)
