from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    def is_displayed(self):
        if self.participant.vars['finished']:
            return False
        else:
            return self.player.role() == "proposer"


class OfferWait(WaitPage):
    pass

class Response(Page):
    form_model = 'group'
    form_fields = ['response']

    def is_displayed(self):
        if self.participant.vars['finished']:
            return False
        else:
            return self.player.role() == "responder"

    def before_next_page(self):
        print("checking payoffs")
        if self.group.response == "accept":
            players = self.group.get_players()

            for p in players:
                p.participant.vars['finished'] = True



class ResponseWait(WaitPage):
    after_all_player_arrive = "check_payoffs"

class Results(Page):
    def is_displayed(self):
        if self.participant.vars['finished'] == False:
            return True
        elif self.round_number in [4,8]:
            return True
        else:
            return False

class BeforeNextPartner(WaitPage):

    def is_displayed(self):
        return self.round_number == 4


class NextPartner(Page):
    def is_displayed(self):
        return self.round_number == 4

    def before_next_page(self):
        players = self.group.get_players()
        for p in players:
            p.participant.vars['finished'] = False

        print("Resetting finished")

page_sequence = [Offer, OfferWait, Response, ResponseWait, Results, BeforeNextPartner, NextPartner]
