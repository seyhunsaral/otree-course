Homogenous Groups
=================
In this part we will talk about groups with heterogeneous members. Which means every group member will have the same role in the game. 


First let's talk about the differences between individual tasks and such a heterogeneous group task.

| Aspect                     | Individual task        | Group Task                                     |
| -----------------          | ------------------     | --------                                       |
| **variables/calculations** | Only my own variable   | I need to reach other peoples variables        |
| **pages**                  | I can have my own pace | Sometimes have to wait for other group members |



The `Group` class in oTree handles much of the structure required by groups. The number of players in a group in an app is determined by the `players_per_group` variable in the `Constants` classs in models.py. 

```
class Constants(BaseConstants):
    # ...
    players_per_group = 3
    # ...
    
```

By default, groups are fixed and determined by the ID of a player in a subsession (which is assigned internally). We will cover different matching procedures in the {ref}`heterogeneous-groups` and {doc}`./matching` sections.


## `Player` and `Group` classes

```{figure} ../figures/classes.png
---
name: classes
---
Demonstration of models: `Player` class and `Group` class
```

## `player` and `group` instances
```{figure} ../figures/instances.png
Instances of classes
```

## `How those instances stand in the bigger picture`
```{figure} ../figures/instances_detail.png
Instances of classes: We will talk in detail on the next lectures
```


## oTree object model
```{figure} ../figures/object_model_self.png
Object model. Source: [oTree Documentation - Conceptual Overview](https://otree.readthedocs.io/en/latest/conceptual_overview.html#self-extended-examples)
```

### Reaching other objects 

### `Player` class
```
class Player(BasePlayer):

    def example(self):

        # current player object
        self

        # method you defined on the current object
        self.my_custom_method()

        # parent objects
        self.session
        self.subsession
        self.group
        self.participant

        self.session.config

        # accessing previous player objects
        self.in_previous_rounds()

        # equivalent to self.in_previous_rounds() + [self]
        self.in_all_rounds()
```

### `Group` class
```
class Group(BaseGroup):
    def example(self):

        # current group object
        self

        # parent objects
        self.session
        self.subsession

        # child objects
        self.get_players()


```

### `Page` class
```
class MyPage(Page):
    def example(self):

        # current page object
        self

        # parent objects
        self.session
        self.subsession
        self.group
        self.player
        self.participant
        self.session.config
```

