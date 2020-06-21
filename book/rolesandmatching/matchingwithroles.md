Matching with Roles
=================


## Random matching when the roles are constant 
In the {ref}`trust-game` and the {ref}`section-roles` sections, we defined the roles based on the player attribute `id_in_group`. This is the easiest and the most convenient way most of the time. As we seen previously this can work out of the box. 


```{figure} ../figures/mtc_same_group_same_role.png
---
name: same_group_same_role
height: 500px
---
Default matching when we have the roles defined on `id_in_group`. 1 for red player , 2 for green player.
```


However recall that, in the random matching example in the previous page, `Player 1` and all the other players can be either in the first or the second position in their group list. Their position in their group coincides with their `id_in_group`.



In some cases we would like to keep the `id_in_group` constant for each player. Luckily, `group_randomly()` have a feature to shuffle the groups while keeping the `id_in_group` constant.

```{figure} ../figures/mtc_random_matching_id.png
---
name: random_matching_id
height: 500px
---
The method with the argument, `group_randomly(fixed_id_in_group=True)` shuffles players in a way that each player is in the same id as before.
```


We can obtain this behavior by adding `fixed_id_in_group=True` argument in `group_randomly`: 

```
class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

```

We can also confirm with our output of `get_group_matrix()`:
```
== Round  1  == 
  Matching:  [[<Player  3>, <Player  2>], [<Player  1>, <Player  4>], [<Player  5>, <Player  6>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  4>], [<Player  3>, <Player  6>], [<Player  5>, <Player  2>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  6>], [<Player  5>, <Player  4>]]
```

So our matching looks something like this:
```{figure} ../figures/mtc_random_group_same_role.png
---
name: random_matching_id
height: 500px
---
The method with the argument, `group_randomly(fixed_id_in_group=True)` shuffles players in a way that each player is in the same id as before.
```




# Putting it all together: Defining roles

* Let's say we would like to have two roles: `red` and `green`
* We would like to shufle groups in the first round keep constant for the rest.

Our `models.py` would look like this:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly(fixed_id_in_group=True)
        else:
            self.group_like_round(1)
        
        print("== Round " , self.round_number, " == ")
        print("  Matching: ", self.get_group_matrix())

        if self.round_number == Constants.num_rounds:
            print("\n\n")

class Group(BaseGroup):

    pass


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'red'
        if self.id_in_group == 2:
            return 'green'

```



```
== Round  1  == 
  Matching:  [[<Player  1>, <Player  4>], [<Player  3>, <Player  6>], [<Player  5>, <Player  2>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  4>], [<Player  3>, <Player  6>], [<Player  5>, <Player  2>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  4>], [<Player  3>, <Player  6>], [<Player  5>, <Player  2>]]

```

# Using `set_group_matrix()`
    * We can give a specific matching structure by using `set_group_matrix()` method in `Subsession` class. As `get_group_matrix()` gives us a nested list of groups of player objects, we should constract the same structure.
    
    * To do that, first we need to get player objects (`self.get_players()` or the original matrix (`self.get_group_matrix()`)

    * We can also do that by providing a nested list of integers instead of player objects. Each integer represents player's `id_in_subsession`. For instance:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        grouping = [[1,2],[4,3],[5,6]]
        self.set_group_matrix(grouping)

```

This gives us the output:


```
== Round  1  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  4>, <Player  3>], [<Player  5>, <Player  6>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  4>, <Player  3>], [<Player  5>, <Player  6>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  4>, <Player  3>], [<Player  5>, <Player  6>]]
== Round  4  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  4>, <Player  3>], [<Player  5>, <Player  6>]]
```


