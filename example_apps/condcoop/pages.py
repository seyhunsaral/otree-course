from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class CondCoop(Page):
    form_model = 'player'
    form_fields = ['cc_0', 'cc_1', 'cc_2', 'cc_3', 'cc_4', 'cc_5']

    def before_next_page(self):
        self.participant.vars['cond_coop'] = [self.player.cc_0, self.player.cc_1, self.player.cc_2, self.player.cc_3, self.player.cc_4, self.player.cc_5 ]
        self.player.payoff = 100

    def app_after_this_page(self, upcoming_apps):
        if sum(self.participant.vars['cond_coop']): # if my sum is positive.
            return upcoming_apps[-1]  # go to the last app


page_sequence = [CondCoop]
