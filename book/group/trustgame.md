(trust-game)=
Practice: Trust Game
====================
(The code was adapted from the oTree documentation)
We will create a Trust game in which we will have two players with different roles and those players will enter different pages. 



```{figure} ../figures/trust_game_str.png
---
name: trust_game_str
---
Trust Game Structure
```

| Stage   | Page         | Description                                                                   |
|---------|--------------|-------------------------------------------------------------------------------|
| Stage 1 | Send         | First player chooses to send points between `0` and `10`.                     |
|         | WaitingForP1 | The amount sent by the first player will be tripled .                         |
| Stage 2 | SendBack     | Second player will decide to send a number of points back to the first player |
|         | WaitingForP2 |                                                                               |
| Stage 3 | Results      | They will both see the final payoffs.                                         |

```{figure} ../figures/trust_ss4.png
---
name: trust_game_ss1
---
Decision Screen of P1 : `Send` page
```


```{figure} ../figures/trust_ss3.png
---
name: trust_game_ss2
---
Decision Screen of P2 : `SendBack` page
```



```{figure} ../figures/trust_ss2.png
---
name: trust_game_ss3
---
Results screen as it is shown to P1: `Results` page
```

```{figure} ../figures/trust_ss1.png
---
name: trust_game_ss4
---
Results screen as it is shown to P2: `Results` page
```





## Game Parameters
| Parameter             | Description                           | Scope     | Field/Type       |
| -------------         | ----------------------------------    | --------  | ----------       |
| players_per_group     | (built-in) Number of players in group | Constants |                  |
| endowment             | Initial endowment of PI               | Constants | Currency `c()`   |
| multiplication_factor | The multiplier of P1's transfer to P2 | Constants |                  |
| sent_amount           | The amount sent by P1 to P2           | Group     | **IntegerField** |
| sent_back_amount      | The amount sent back by P2 to P1      | Group     | **IntegerField** |


* Let's create our empty app:
```
otree startapp trust
```
## `models.py`

* Go to `models.py`:
  * We modify the attribute `players_per_group` and add `endowment` and `multiplication_factor`
  
```
class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3
```

  * Then let's add fields for `sent_amount` and `sent_back_amount` in Group class. 
  
```
class Group(BaseGroup):
    sent_amount = models.CurrencyField(label = "How much would you like to send to Player 2?", min=c(0), max=c(10))
    sent_back_amount = models.CurrencyField(label = "How much would you like to send back to Player 1?", min=c(0))
```

```{warning}
Please note that we use a `CurrencyField` instead of `IntegerField` and we set the minimum and maximum values as currencies (`c(0)` and `c(10)`) accordingly.
```
  * We still need to determine the min and max for `sent_back_amount`. This is not straightforward because by the time our class definition runs, we don't know how many points Player 1 sent, and how many points will be available for P2 to be sent back. oTree has an option to determine minimum, maximum and possible choices of a field dynamically. ([See here for the relevant part in documentation](https://otree.readthedocs.io/en/latest/forms.html?highlight=_max()#dynamic-form-field-validation)). For this, we will define the method `sent_back_amount_max()`. So our `Group` class looks like this:
  
```
class Group(BaseGroup):
    sent_amount = models.CurrencyField(label = "How much would you like to send to Player 2?", min=c(0), max=c(10))
    sent_back_amount = models.CurrencyField(label = "How much would you like to send back to Player 1?", min=c(0))
    
    def sent_back_amount_max(self):
        return self.sent_amount * Constants.multiplication_factor

```

  * We have one more step until we are done with the `models.py` which is the function to handle the payoffs: `set_payoffs()`. We should define it under the Group method because we are going to call it by using `after_all_players_arrive` attribute in our page later on. 
    * Here we can get each player, P1 and P2 in the group separetely. P1 is going to be our trustor, and P2 is going to be the trustee. 
    
    ```
    def set_payoffs(self):
        p1 = self.get_player_by_id(1) # Get the first player in group
        p2 = self.get_player_by_id(2) # Get the second player in group
        

        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount 
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount
    
    ```

  * Player 1 gets the points he didn't transfer at the first stage plus what was sent back by Player 2.
  * Player 2 gets the points she received by what Player 1 transferred to her multiplied by 3, minus the amount she transferred back to him.

* The final `models.py` looks like this:

```
# ==== These parts were generated by oTree =====
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
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(label = "How much would you like to send to Player 2?", min=c(0), max=c(10))
    sent_back_amount = models.CurrencyField(label = "How much would you like to send back to Player 1?", min=c(0))

    def sent_back_amount_max(self):
        return self.sent_amount * Constants.multiplication_factor

    def set_payoffs(self):
        p1 = self.get_player_by_id(1) # Get the first player in group
        p2 = self.get_player_by_id(2) # Get the second player in group
        
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount 
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount
        
        
class Player(BasePlayer):
    pass


```
## `pages.py`

* As we planned at the beginning we will have 5 pages: `Send`, `WaitingForP1`, `SendBack`, `WaitingForP2`, `Results`. We have two pages with special display conditions: `Send` page only to be displayed to Player 1, and `SendBack` page only to be displayed to Player 2. 

* Waiting pages have two functions: Provides a place to wait while the other player decides, makes sure the calculations are made after we acquired the necessary information from the other player. 

* We start by defining `Send` page as usual. We have one form to fill, that is `sent_amount` in the group model:

```
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']
```

* `is_displayed` on that page is a user-defined function which should return `True` if the player should see the page. We only want P1, whose `id_in_group` is 1, to see the page. Therefore our `Send` page becomes this:

```
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1
```

* We define the `WaitingForP1`. We just need to add the page inherited from `WaitPage` class. We don't need any calculations here:

```
class WaitForP1(WaitPage):
    pass
```

* Next we need to add `SendBack`. It has a very similar structure to `Send`. But this time the form field we want to show the user is `send_back_amount` and this page whould be seen only by P2:

```
class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

```

* We add the following `WaitPage` but this time we will make the payoff calculations after P2 finishes his decision. This will be triggered by `after_all_players_arrive` method which will call our `set_payoffs()` function.

```
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
```

* And finally we add Results page. We don't need to add anything specific here. 

```
class Results(Page):
    pass
```

We should not forget to update `page_sequence` after we defined our pages. It should look like this:

```
page_sequence = [Send, WaitForP1, SendBack, ResultsWaitPage, Results]
```

## Templates

* We add a template for `Send`, a template for `SendBack` and a template for `Results`. The first one is straightforward. So I will add the code below. As usual our templates goes in the subfolder with the app name in the templates folder (`./templates/trust/Send.html`) in the app:

```
{% extends "global/Page.html" %}
{% load otree static %}


{% block title %}
Please make a decision
{% endblock %}

{% block content %}

<p>
  You are selected as Player 1. You have {{Constants.endowment }} points. 
  You can transfer some amount of it to Player 2.
</p>

{% formfields %}

{% next_button %}


{% endblock %}


```

* In a similar way we build `SendBack.html` but we would like to show the amount available for Player 2 to make the the transfer. This amount was calculated as `sent_amont * Constants.multiplication_factor` earlier in the `set_payoffs` function. But we don't have it in our model and for us to show it in the template (as we cannot make calculations in the template), we should define `vars_for_template` and input that calculation into our template. Thus we should go back to `pages.py` to add the last two lines below:
```
class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return dict(tripled_amount=self.group.sent_amount * Constants.multiplication_factor)
```

Then we can create `./templates/trust/SendBack.html`:

```
{% extends "global/Page.html" %}
{% load otree static %}


{% block title %}
Please make a decision
{% endblock %}

{% block content %}

<p>
  You are selected as Player 2.
  Player 1 chose to transfer you {{ group.sent_amount }} points thus you have {{tripled_amount}} points.
</p>

{% formfields %}

{% next_button %}


{% endblock %}
```

* Finally we show the results to players (`./templates/trust/Results.html`). We can use the if conditions in order to show the information in a customized way easily:

```
{% extends "global/Page.html" %}
{% load otree static %}

{% block title %}
Results
{% endblock %}

{% block content %}
{% if player.id_in_group == 1 %}
<p>
  You sent Participant 1 {{ group.sent_amount }}.
  Participant 2 returned {{ group.sent_back_amount }}.
</p>
{% else %}
<p>
  Participant 1 sent you {{ group.sent_amount }}.
  You returned {{ group.sent_back_amount }}.
</p>

{% endif %}

<p>
  Your payoff is {{ player.payoff }}.
</p>
    
{% endblock %}


```

* So this concludes the core of our game. We can improve the game in certain ways and of course visually. We will leave this to you at the moment until we cover styling in our next sessions.
