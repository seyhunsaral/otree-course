from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    def is_displayed(self):
        if self.participant.vars['is_finished']:
            return False
        else:
            return self.player.role() == 'proposer'

class WaitOffer(WaitPage):
    pass

class MatchInfo(Page):
    timeout_seconds = 3

    def is_displayed(self):
        return self.round_number in [1,5]

    def before_next_page(self):
        self.participant.vars['is_finished'] = False
        print("executred before_next_page")



class Response(Page):
    form_model = 'group'
    form_fields = ['response']

    def js_vars(self):
        return dict(offer = self.group.offer, current_pie = self.group.current_pie)
    
    def is_displayed(self):
        if self.participant.vars['is_finished']:
            return False
        else:
            return self.player.role() == 'responder'

    def before_next_page(self):
        print("checking payoffs")
        if self.group.response == "accept":
            
            for p in self.group.get_players():
                p.participant.vars['is_finished'] = True

                if p.role() == 'proposer':
                    proposer_payoff = p.group.current_pie - p.group.offer 
                #    p.payoff = proposer_payoff
                    p.participant.vars['payoff_list'].append(proposer_payoff)
                    
                if p.role() == 'responder':
                #    p.payoff = p.group.offer
                    responder_payoff = p.group.offer
                    p.participant.vars['payoff_list'].append(responder_payoff)

        if self.group.response == "reject" and self.round_number in [4,8]:
            for p in self.group.get_players():
                p.participant.vars['payoff_list'].append(c(0))

            

class WaitResponse(WaitPage):
    pass


class Results(Page):

    def vars_for_template(self):
        return dict(proposer_payoff = self.group.current_pie - self.group.offer)


    def is_displayed(self):
        print("payoff list for",self.participant.id_in_session, self.participant.vars['payoff_list'])
        return self.group.response in ["accept", "reject"]

        
class BeforeFinalResults(WaitPage):
    after_all_players_arrive = 'set_payoffs'


    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class FinalResults(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [MatchInfo, Offer, WaitOffer, Response, WaitResponse, Results, BeforeFinalResults, FinalResults]
