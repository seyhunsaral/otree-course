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
    name_in_url = 'guesstheaverage'
    players_per_group = 3
    num_rounds = 1
    reward = c(20)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    average_guess = models.FloatField()

    def set_payoffs(self):
        players = self.get_players()
        guesses = [p.guess for p in players]
        self.average_guess = sum(guesses) / len(guesses)

        for p in players:
            p.distance = abs(p.guess - self.average_guess)

        distances = [p.distance for p in players]

        min_distance = min(distances)

        for p in players:
            if p.distance == min_distance:
                p.is_winner = True
                p.payoff = Constants.reward




class Player(BasePlayer):
    guess = models.IntegerField(min=0, max=100)
    is_winner = models.BooleanField(initial=False)
    distance = models.FloatField()
