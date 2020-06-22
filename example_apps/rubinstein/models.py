from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Ali Seyhun Saral'

doc = """
Rubinstein bargaining

* Partner matching for 4 rounds, rematch, another partner matching for 4 rounds
"""


class Constants(BaseConstants):
    name_in_url = 'rubinstein'
    players_per_group = 2
    num_rounds = 8
    
    initial_pie = c(100)
    dimninshing = c(25)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            players = self.get_players()
            for p in players:
                p.participant.vars['finished'] = False

        if self.round_number in [1,5]:
            self.group_randomly()
            
            

        else:
            if self.round_number < 5:
                self.group_like_round(1)
            elif self.round_number > 5:
                self.group_like_round(5)
                
        print(self.get_group_matrix())

        for g in self.get_groups():
            if self.round_number < 5:
                g.current_pie = Constants.initial_pie - ((self.round_number -1) * Constants.dimninshing)
            if self.round_number >= 5:
                g.current_pie = Constants.initial_pie - ((self.round_number -5) * Constants.dimninshing)


class Group(BaseGroup):
    current_pie = models.CurrencyField()

    offer = models.CurrencyField(min=0, max=current_pie, label="Please write how much would you like to offer the other player",
                                 widget=widgets.Slider(show_value=True))

    response = models.StringField(label= "Please tell us would you rather accept or reject the offer?", choices=[["accept", "Accept the Offer"],["reject", "Reject the Offer"]])
    
    def offer_max(self):
        return self.current_pie


class Player(BasePlayer):
    def role(self):
        if self.round_number % 2 == 0:
            return { 1: 'proposer', 2: 'responder'}[self.id_in_group]
        else:
            return { 1: 'responder', 2: 'proposer'}[self.id_in_group]

