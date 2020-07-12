from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    def js_vars(self):
        return dict(cond_coop = self.participant.vars['cond_coop'])

page_sequence = [Results]
