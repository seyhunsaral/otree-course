Matching with Roles
=================


## Random matching when the roles are constant[^1]
In the {ref}`trust-game` and the {ref}`section-roles` sections, we defined the roles based on the player attribute `id_in_group`. This is the easiest and the most convenient way most of the time. As we seen previously this can work out of the box. 

```{figure} ../figures/mtc_same_group_same_role.png
---
name: same_group_same_role
height: 500px
---
Default matching when we have the roles defined on `id_in_group`. 1 for red player , 2 for green player.
```



Notice that `Player 1` and all the other players can be either in the first or the second position in their group list. Their position in their group coincides with their `id_in_group` as well. 

In some cases we would like to keep the `id_in_group` constant for each player 
