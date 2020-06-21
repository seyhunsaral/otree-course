from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Guessing(Page):
    form_model = 'player'
    form_fields = ['guess']

class AfterGuessing(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    def vars_for_template(self):
        guesses = [p.guess for p in self.group.get_players()]
        return dict(guesses = guesses)



page_sequence = [Guessing, AfterGuessing, Results]
