Practice: Managing roles
========================

## Fixed number in roles in fixed groups
* Let's create a group with 2 buyers and 2 sellers.

```
otree startapp role_practice
```

* Go to `models.py` and change `players_per_group` in `Constants` model to `4`.
```
class Constants(BaseConstants):
    name_in_url = 'role_practice'
    players_per_group = 4
    num_rounds = 1
```


* Go to `Player` class and define roles:

```
class Player(BasePlayer):

    def role(self):
        if self.id_in_group <= 2:
            return 'buyer'
        if self.id_in_group > 2:
            return 'seller'
        
```

* Let's go to `pages.py` and remove the pages `MyPage` and `ResultsWaitPage`. Having a single page would be enough for our purposes and we can check the role from oTree admin panel. Our `pages.py` should look like this:

```
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    pass


page_sequence = [Results]
```

* And let's add our app to `settings.py`:

```
SESSION_CONFIGS = [
    # other configs
     dict(
        name='role_practice',
        display_name="role_practice",
        num_demo_participants=4,
        app_sequence=['role_practice'],
     ),
]
```

So when we create the session with 8 participants from oTree control panel

```{figure} ../figures/setting_up_session.png
```

And when we go to the data we see that roles are set as we want them to be:

```{figure} ../figures/roles_regular.png
```

We can also shorten the if conditions as the following:


```
    def role(self):
        return {1: 'buyer', 2: 'seller'}[self.id_in_group]
```

## Balanced number of roles in a variable group size
* Imagine that we have a variable group size (for instance group size is a treatment variable). And we would like to balance our 3 roles. (say `buyer`, `seller`, `observer`). We have several possibilities to go for. 


````{admonition} Python Break - Modulus
* Modulus operator is used to get the remainder of a division.
* Usage: `Number % Divisor`

   ```{code-block} python
   10 % 2  # returns 0
   10 % 4  # returns 2
   ```
````


We will use modulus operator `%` in order to give a balanced number of roles:

```
    def role(self):
        roles = ['buyer', 'seller', 'observer']
        num_roles = len(roles)
        if self.id_in_group % num_roles == 0:
            return roles[0]
        if self.id_in_group % num_roles == 1:
            return roles[1]
        if self.id_in_group % num_roles == 2:
            return roles[2]
```
Which can be reduced to:

```
    def role(self):
        roles = ['buyer', 'seller', 'observer']
        num_roles = len(roles)
        return roles[(self.id_in_group -1) % num_roles]  # added -1 to start from the first element in the list
```

* Then for the size `3`:


```{figure} ../figures/roles_3_players.png
```

* And for the size `7`:


```{figure} ../figures/roles_7_players.png
```

### Fixed roles in each round/app

In order to fix a role, we can store it in our `participant.vars`. 

```
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
    
```

One final note: For the multiple round cases, you can fix `id_in_group` in a random matching by `group_randomly(fixed_id_in_group=True).`
