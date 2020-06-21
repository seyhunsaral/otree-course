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
    name_in_url = 'role_practice'
    players_per_group = 3
    num_rounds = 5


class Group(BaseGroup):
    def do_something(self):
        print(self.get_players())

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly() # This randomizes the groups
            
        # Some role assignment below
        for p in self.get_players():
            if self.round_number == 1:
                if p.id_in_group % 2 == 0:
                    p.participant.vars['type'] = 'buyer'
                else:
                    p.participant.vars['type'] = 'seller'
    
            p.type = p.participant.vars['type']

class Player(BasePlayer):
    def role(self):
        return self.participant.vars['type']

    type = models.StringField()
