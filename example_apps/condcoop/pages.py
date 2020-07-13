from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Slider(Page):
    form_model = 'player'
    form_fields = ['contribution']


class CondCoop(Page):
    form_model = 'player'
    form_fields = ['cc_0', 'cc_1', 'cc_2', 'cc_3', 'cc_4', 'cc_5']

    def before_next_page(self):
        self.participant.vars['cond_coop'] = [self.player.cc_0, self.player.cc_1, self.player.cc_2, self.player.cc_3, self.player.cc_4, self.player.cc_5 ]
        self.player.payoff = 100




page_sequence = [Slider, CondCoop]
