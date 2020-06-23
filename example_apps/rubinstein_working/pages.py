from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    def is_displayed(self):
        return self.player.role() == 'proposer'

class WaitOffer(WaitPage):
    pass


class Response(Page):
    form_model = 'group'
    form_fields = ['response']


    def is_displayed(self):
        return self.player.role() == 'responder'


class WaitResponse(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Offer, WaitOffer, Response, WaitResponse, Results]
