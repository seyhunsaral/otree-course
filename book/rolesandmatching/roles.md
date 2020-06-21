(section-roles)=
Roles
=====
Another option is to manage heterogeneous groups is to use the **self-defined** built-in function `role()`. 

The `role()` method should be defined under `Player` classs in `models.py` and the method should return a string indicating the role of the player. For instance:

```
def role(self):
    if self.id_in_group == 1:
        return 'trustor'
    if self.id_in_group == 2:
        return 'trustee'
        
```

Then you can get the **first player** with the certain role using `get_player_by_role()` function. For instance:

`trustee = get_player_by_role('trustee')`

````{warning}
It is a common mistake to treat random as an attribute instead of a method. So you should call it including the parantheses:

```
if self.player.role() == 'buyer':
    # do things
    
# This is correct
```

instead of calling it directly: 

```
if self.player.role == 'buyer':
    # do things
    
# This is incorrect!
```
````

You can also use a random mechanism to determine the roles and call it in the role function:

```
import random 

class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.random_value = random.random() # Returns a value between 0 and 1

class Player(BasePlayer):
    # Other things here
    
    def role(self):
    if self.random_number > 0.5:
        return 'buyer'
    if self.id_in_group <= 0.5:
        return 'seller'
```


````{warning}
Note that `get_player_by_role` returns a single player only. You should only use it when you have a single player with the certain role. Therefore if you have to get a list of players with the same role, you should loop over players list. 
For instance:
```
class Group(BaseGroup):
    def do_something(self):
        all_players = self.get_players()
        
        sellers = []
        for p in self.get_players():
            if p.role() == 'seller':
                sellers.append(p)
        
        print(sellers)

# gives the output 
# [<Player  2>, <Player  5>, <Player  8>, 
#  <Player 11>, <Player 14>, <Player 17>, 
# <Player 20>, #  <Player 23>, <Player 26>]

```
If you use it very often, you can just define it as a method on your `Group` class.

```
class Group(BaseGroup):
    def get_players_by_role(self, role):
        subgroup = []

        for p in self.get_players():
            if p.role() == role:
                subgroup.append(p)
        return subgroup
```

````

## `participant.vars` as a place to store the roles

In an experiment, it is often you regroup participants or you have several apps. And sometimes you'd like to keep the roles fixed during the course of the game. As we often define group by using `id_in_group` attribute and it is subject to change, we need to store the information for the role in a fixed place. 

In oTree (recall from the architecture section), the `player` object is recreated in each app/round. But every participant have a fixed object called `participant`. 

Each participant object have a dictionary `vars` in which you can store a key value pair as you'd like. Then you can access to this variable during the course of the experiment at any time. For instance:

```
self.participant.vars['my_type'] = 'seller`
```

```{warning}
Neither the values from `participant.vars` nor `role()` method are included in the data export. If you'd like to have them in your data, you should save them in a variable in your model.

```
