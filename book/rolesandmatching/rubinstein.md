(rubinstein-bargaining)=
Practice: Rubinstein Bargaining Game
=====================================

We will create a Rubinstein Bargaining Game with follwing properties:

* The pie to bargain on: 100 ECU
* Two players: One proposes, one accepts/rejects
* If the responder accept the proposal, they recieve the relevant amount. If not in the next round:
  * They swith roles
  * The pie dimnishes by 25 ECU
* If there is no agreement, the game stops after the 4th round. (When the total pie is over)

* In our game we will have two separate games. The players play the game twice with different partners.


# Planning the game

## Pages
<!--
```{figure} ../figures/trust_game_str.png
---
name: trust_game_str
---
Trust Game Structure
```
-->
| Page         | Description                                      |
|--------------|--------------------------------------------------|
| MatchInfo    | Display informaiton about matching               |
| Offer        | Proposer offers an amout between `0` and `100`   |
| WaitOffer    | Responder waits                                  |
| Response     | Responder accepts or rejects the offer           |
| WaitResponse | Proposer waits                                   |
| Results      | They will both see whether it is accepted or not |
| FinalResults | They will see the final payoffs                  |


## Variables in `models.py`

| Variable          | Description                                        | Scope     | Field/Type              |
| -------------     | ----------------------------------                 | --------  | ----------              |
| players_per_group | (built-in) Number of players in group              | Constants |                         |
| num_rounds        | (built-in) Number of rounds                        | Constants |                         |
| initial pie       | Initial amount to divide                           | Constants | Currency `c()`          |
| dimnisihing       | The amount of pie dimnishes each round             | Constants | Currency `c()`          |
| role              | `"proposer"` or `"responder"`                      | Player    | Method returning string |
| offer             | The amount offered by proposer                     | Group     | **CurrencyField**       |
| sent_back_amount  | The response of responder `"accept"` or `"reject"` | Group     | **CurrencyField**       |
| current_pie       | Current size (undimnished part) of the pie         | Group     | **CurrencyField**         |


# Building the game

## Constants 
We start by defining constants in our `models.py`. Nothing tricky there:

```
    name_in_url = 'rubinstein'
    players_per_group = 2
    num_rounds = 8

    initial_pie = c(100)
    dimnishing = c(25)
```

## Group variables
* We define the variables in `models.py` as we planned:

```
class Group(BaseGroup):
    offer = models.CurrencyField(min=0, label = "How much would you like to offer?")
    response = models.StringField(choices = ["accept", "reject"], label = "Please tell your response",)
    current_pie = models.CurrencyField()
```

Note that we didn't define the maximum offer because as the pie decreases each round, we should define it dynamically. For this purpose we should create a method called `offer_max`. oTree recognizes the format `FIELDNAME_max` so, it runs the method when the page is loaded and submitted and checks whether the input is valid. (See [Forms - Determining form fields dynamically](
https://otree.readthedocs.io/en/latest/forms.html?highlight=dynamically%5C#field-name-max) for details.)

We define it by this method in `Group` class:

```
    def offer_max(self):
        self.current_pie = Constants.initial_pie - ((self.round_number -1) % 4 )* Constants.dimnishing
        return self.current_pie


```



## Matching
* We have a particular matching structure:
  * Players will be grouped randomly in round 1
  * They will play with the same partner until the pie dimnishes (4 rounds)
  * They will be matched with another partner in round 5
  
This can be done with the `group_randomly()` and `group_like_round()` methods in `Subsession` class in `models.py`. 

```
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number in [1,5]:
            self.group_randomly()
        else:
            self.group_like_round(self.round_number -1)

        print(self.get_group_matrix()) # Here we add the print statement so we can actually see it.
```

## Roles
We want roles to be switched in each round, ie, the player who was the proposer should be the responder in the second round (if exists) and proposer again in the third round and so on. We can rely on `id_in_group` attribute in `Player` class. So:

```
class Player(BasePlayer):
    def role(self):
        if self.round_number % 2 == 1:
            return {1: 'proposer', 2: 'responder'}[self.id_in_group]
        else:
            return {2: 'proposer', 1: 'responder'}[self.id_in_group]
```

Here we use the modulus operator (`%`) which lets us to check if the round number is even or odd.


So far we are done with the `models.py` for the basic functionality. We will return here later.

# Pages 

First we create the pages with form input:

## Offer page

```
class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    def is_displayed(self):
        return self.player.role() == 'proposer'
        
        
class Response(Page):
    form_model = 'group'
    form_fields = ['response']


    def is_displayed(self):
        return self.player.role() == 'responder'
```

These pages has nothing particular except the display condition `is_diplayed` for each role. And we add the rest of the pages with even less input.


```
class WaitOffer(WaitPage):
    pass


class WaitResponse(WaitPage):
    pass


class Results(Page):
    pass
    ```
    
And we add the page sequence:
```
page_sequence = [Offer, WaitOffer, Response, WaitResponse, Results]
```


