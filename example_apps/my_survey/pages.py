from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    pass

class Survey(Page):
    form_model = 'player'
    form_fields = ['name', 'age', 'is_student', 'department']

class Lottery(Page):
    form_model = 'player'
    form_fields = ['risky_selected']

    def before_next_page(self):
        self.player.set_payoffs()

class Results(Page):
    pass

page_sequence = [#Welcome,
                 Survey, Lottery, Results]
