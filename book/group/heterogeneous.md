(heterogeneous-groups)=
Heterogenous Groups
===================
In the previous sections, we learned how the groups work and we build a 2 players game where each individual had the identical role and saw identical screens. 

In this section, we will focus on the case when the players have different roles. Games with heterogeneous agents have some unique aspects we need to handle:

* We should be able to identify each player in group in order to give them role-specific tasks object
* We should be able to show each player different screens 


## Identifying participants in group: `id_in_group` 
`oTree` comes with a very hand set of attributes and methods in order to deal with groups. 

The first one is the `player.id_in_group`. In a group each player gets an id, which is an integer that allows us to identify different participants in a group. 


```{figure} ../figures/group_id_in_group1.png
---
name: group_id_in_group
---
Values of `id_in_group` in a 3 player game with 9 participants. We can call each player by the id, thus can define specific roles by using those ids. 
```

By setting the number of players in each group, each player will have the unique integer starting from `1` to `players_per_group`.  We can use `id_in_group` to define the role of a player. For instance, if the players move sequentially, we can give the first move to the player which have the `id_in_group` is equal to 1 in each group. 

We can then get player by their id, using the function `get_player_by_id(n)`. For instance if we'd like to add `10 points ` to the payoff of the player which has the id `2` we can write:

```
second_player = get_player_by_id(2)
second_player.payoff += c(10)

```

```{warning}
Please note that `get_player_by_id` returns the player object which we can use directly, while `get_players()` function returns a list of player objects which we usually need to loop over.
```

## Showing specific pages to specific players: `is_displayed()`
`is_displayed` method in a page is a **user-defined** method to determine if the page is shown to a player or not. If the method returns `True` for the player, the page will be shown to the player. For instance, if we would like to show a page to player with the id `2` we should define the page:

```
class PageForP2(Page):
    # ... other things here ...

    def is_displayed(self):
        return self.player.id_in_group == 1

```

The method `is_displayed` is not necessarily to be defined related with the players. It can be based on a treatment variable or the current round number. For instance:

```
class IntroTreatmentBaseline(Page):
    # ... other things here ...

    def is_displayed(self):
        return self.session.config['treatment'] == "baseline" & self.round_number == 1
```

In the next section, we will build a Trust game using `id_in_group` and `is_displayed()`
