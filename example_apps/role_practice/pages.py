from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    def before_next_page(self):
        self.group.do_something()


page_sequence = [Results]
