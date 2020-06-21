Matching
=========

In this chapter we will discover different matching procedures. Before we continute let's create an app that will allow us to see how the players are matched. 

Let's start with creating the app 

```
otree startapp matching
```

Lets go to `models.py` and set the parameters:

```
class Constants(BaseConstants):
    name_in_url = 'matching_practice'
    players_per_group = 2
    num_rounds = 3
```

Moreover we would like to find a way to see the current matching. In oTree, that is possible `get_group_matrix()` method in the subsession. This method returns a list of list containts player ojects. If we print our the method for instance:

`[[<Player 1>, <Player 2>], [<Player 3>, <Player 4>], [<Player 5>, <Player 6>]]`

This means `Player 1` and `Player 2` is in the same group, `Player 3` and `Player 4` is in the same group and `Player 5` and `Player 6` are in the same group. At the end of this chapter we will see how to manually create such list if we need to and let oTree do the matching accordingly. However at the moment it is enough for us to create this list and print it out for us to see. 

As we know, defining a `creating_session(self)` method in `Subsession` class will trigger this function in each round of the app. (a.k.a. in each subsession). So define the following function in order to see the matching:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        print("== Round " , self.round_number, " == ")
        print("  Matching: ", self.get_group_matrix())
        
```
Now if we run the app directly we will get the following output in our console:
```
== Round  1  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  4>], [<Player  5>, <Player  6>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  4>], [<Player  5>, <Player  6>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  4>], [<Player  5>, <Player  6>]]

```

## The default matching in oTree

```{figure} ../figures/mtc_fixed_matching_default.png
---
name: fixed_matching_default
height: 500px
---
`oTree`'s default matching: Each player is matched sequentially in each round (fixed matching)
```
As we seen in our practice, by default, oTree matches participants according to their player id's: `P1` is matched with `P2`, `P3` is matched with `P4`. 

## Random matching: `group_randomly()`

```{figure} ../figures/mtc_random_matching.png
---
name: random_matching
height: 500px
---
Matching with `group.randomly()` method in `Subsession`. Each player is reshuffled completely.
```

In order to shuffle players, `Subsession` class has the built-in method `group_randomly()`. In order to create it, we need to call it when we create the session. We can do it by calling `self.group_randomly()` in `creating_session(self)` method we defined:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        
        # our previous priting functions below
```

An example output by our printing code can be seen below:

```
== Round  1  == 
  Matching:  [[<Player  6>, <Player  3>], [<Player  4>, <Player  5>], [<Player  2>, <Player  1>]]
== Round  2  == 
  Matching:  [[<Player  2>, <Player  4>], [<Player  1>, <Player  6>], [<Player  3>, <Player  5>]]
== Round  3  == 
  Matching:  [[<Player  4>, <Player  3>], [<Player  5>, <Player  1>], [<Player  2>, <Player  6>]]

```

In our case `Player 1` is matched with `Player 2` in the first round, with `Player 2` in the second round and `Player 5` in the third round.

### Shuffling on the first round only

What if we want to shuffle the participants in a single round (mostly we'd like to do it in round 1), and keep the matching afterwards. 

The first attempt is just add an if condition about the round:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
            
            ## Do not copy, not complete

```

This is correct but not complete. If we take a look at the matching output we printed out, we will see that the randomization is there in the first round as we'd like to, however, oTree switches back to default matching. 

```
== Round  1  == 
  Matching:  [[<Player  2>, <Player  6>], [<Player  4>, <Player  3>], [<Player  5>, <Player  1>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  4>], [<Player  5>, <Player  6>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  2>], [<Player  3>, <Player  4>], [<Player  5>, <Player  6>]]

```

So, in order to keep the matching, we should tell `oTree` to match as period one. This can be done with `group_like_round(ROUNDNUMBER)` method in Subsession class. So to keep the matching as period one we should update our code as:

```
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)

```

And our output confirms that it behaves as we like:

```
== Round  1  == 
  Matching:  [[<Player  1>, <Player  3>], [<Player  5>, <Player  6>], [<Player  4>, <Player  2>]]
== Round  2  == 
  Matching:  [[<Player  1>, <Player  3>], [<Player  5>, <Player  6>], [<Player  4>, <Player  2>]]
== Round  3  == 
  Matching:  [[<Player  1>, <Player  3>], [<Player  5>, <Player  6>], [<Player  4>, <Player  2>]]

```



Notice that `Player 1` and all the other players can be either in the first or the second position in their group list. Their position in their group coincides with their `id_in_group` as well. 

In some cases we would like to keep the `id_in_group` constant for each player 
