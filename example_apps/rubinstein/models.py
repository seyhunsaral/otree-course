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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'rubinstein'
    players_per_group = 2
    num_rounds = 8

    initial_pie = c(100)
    dimnishing = c(25)


class Subsession(BaseSubsession):
    def creating_session(self):
        print("Creating session is executed")
        print(self.round_number)
        print(self.round_number in [1,5])
        if self.round_number in [1,5]:
            self.group_randomly()
            print("Creating session is executed conditionally")

        else:
            self.group_like_round(self.round_number -1)

        print(self.get_group_matrix())

        for p in self.get_players():
            p.participant.vars['payoff_list'] = []




class Group(BaseGroup):
    offer = models.CurrencyField(min=0, label = "How much would you like to offer?", widget = widgets.Slider())
    response = models.StringField(choices = ["accept", "reject"], label = "Please tell your response",)
    current_pie = models.CurrencyField()
    selected_part = models.IntegerField()

#    def calculate_current_pie(self):
#        self.current_pie = 

    def offer_max(self):
        self.current_pie = Constants.initial_pie - ((self.round_number -1) % 4 )* Constants.dimnishing
        return self.current_pie


    def set_payoffs(self):
        import random
        self.selected_part = random.choice([1,2])
        print("running")

        for p in self.get_players():
            p.payoff = p.participant.vars['payoff_list'][self.selected_part - 1]
        
        
        

class Player(BasePlayer):
    def role(self):
        if self.round_number % 2 == 1:
            return {1: 'proposer', 2: 'responder'}[self.id_in_group]
        else:
            return {2: 'proposer', 1: 'responder'}[self.id_in_group]
