from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    timeout_seconds = 10
    def before_next_page(self):
        self.player.payoff = c(10)



page_sequence = [MyPage]
