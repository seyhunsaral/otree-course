Practice: Guess the average game
================================

## Game structure
We will build a simple guessing game. To be specific, a simpler version of a *Keynesian Beauty Contest Game*. 

* There are 3 players in group
* Each player guesses a number between 0 and 100
* The number which is closest to the average wins 20 points. (That happens to be the median guess).

## Building the app
### Stage I - Collecting guesses

* Create the app
  * `otree startapp guesstheaverage`
* Go to `models.py`


```
class Player(BasePlayer):
    guess = models.IntegerField(min=0, max=100)
```

* Delete mypage and create the page
  * I we will ask our users about their guesses so we add `form_model` and `form_fields` 

```
class Guessing(Page):
    form_model = 'player'
    form_fields = ['guess']
```

* Remember that you need a `string` for `form_model` and a `list` for `form fields`

* Create the page `./guesstwothirds/templates/guesstwothirds/Guessing.html`

```
{% extends "global/Page.html" %} {% load otree static %}

{% block title %} Guessing stage {% endblock %}

{% block content %}

You are in a group of some people. You have to tell a number between 0
and 100. The number closest to the average of the group
wins. Please enter your guess below.

    {% formfields %}

    {% next_button %}

{% endblock %}

```

* We can also prepare the template for the results 

```
{% extends "global/Page.html" %}
{% load otree static %}

{% block title %}
    Results
{% endblock %}

{% block content %}
The guesses were:
Your guess was:
The average is:

You win/you didn't win

{% endblock %}

```

* Let's try entering some numbers 


```{figure} ../figures/guess1.png
---
name: guessingdata
---
Here is how the data looks
```
### Group structure is already there
As you can see that we already have a some columns on our data that might be helpful:
**id in group** (attribute `id_in_group`) which is increasing. **role** (method `role`). Then we have a set of columns **id in subsession** (attribute `id_in_subsession`). 

* We will utilize those but lets set the right parameters and fields first in our app. We need to identify which parameters we need and which scope those parametrs have. 

* A rule of thumb to understand the parameters and fields are to answer the question: **"For which group of people this value will be the same?"**. The answer of this question, whether it is the player, group, or everyone (Subsession/Constants) will most likely to be our scope and therefore these values will go to the related class. 

### Considering the groups
As we discussed earlier let's thing of in terms of models. Parameters we need for the guessing game:


| Parameter         | Description                                 | Scope     | Field/Type       |
| -------------     | ----------------------------------          | --------  | ----------       |
| max_guess         | Maximum possible guess                      | Constants |                  |
| min_guess         | Minimum pussible guess                      | Constants |                  |
| players_per_group | (built-in) Number of players in group       | Constants |                  |
| reward            | Reward if the number is correct             | Const     | Currency         |
| guess             | The number guessed by the person            | Player    | **IntegerField** |
| is_winner         | Dummy if the player is the winner           | Player    | **BooleanField** |
| average_guess     | The average of all guesses in group         | Group     | **FloatField**   |
| proximity         | Difference between my guess and the average | Player    | **FloatField**   |



Lets go to `models.py` and implement those:

```
class Constants(BaseConstants):
    name_in_url = 'guesstheaverage'
    players_per_group = 3
    num_rounds = 1
    max_guess = 0
    min_guess = 100
    reward = c(20)
```

```
class Group(BaseGroup):
    average_guess = models.FloatField()
```

And we should update the limits of our guess field in our player model. We can also add a label to it.

```
class Player(BasePlayer):
    guess = models.IntegerField(min=Constants.min_guess,
                                max=Constants.max_guess, 
                                label = "Your number")
                                
    proximity = models.FloatField()

    is_winner = models.BooleanField(initial=False)

```


Let's see how it looks:

```{figure} ../figures/guess2.png
---
name: withoutwaitpage
---
Players jump to results screen
```

It seems that the first player passes to the results while the second and third player is making a decision still. The problem here is that we don't have a moment after all the players make the decisions to calculate the average.

For this purpose, oTree has a parent class "WaitingPage". So we create a waiting page on `pages.py`  similar to how we create regular pages, to make sure that everybody passes to the next page after everybody arrives. 

```
class AfterGuessing(WaitPage):
    pass
```

```
page_sequence = [Guessing, AfterGuessing, Results]
```

```{figure} ../figures/guess3.png
---
name: waitpageinserted
---
With the `AfterGuessing` (which is inherited from `WaitPage`) the players who completed the page are forced to wait until other players arrive.
```

```{admonition} WaitPage in oTree
* `WaitPage` is used for stopping the rest of the players until the rest of the players arrive to the same page. 

* The default scope of it is `group`. (Players in the same group wait.)

* Attribute under the page class `wait_for_all_groups = True` extends the scope to `subession`. (Players in the same subsession wait).

* The attribute `after_all_players_arrive = 'function_name'` allows you to run a function once all players are there. This takes the stated function in `Group` class. 


* You can change the title and the text in the waiting page by setting `title_text` and `body_text`

```

```{warning}
The method `after_all_players_arrive` only works in `WaitPage`, as opposed to a regular `Page`
```


Now that we use wait pages and we can run a function after all players arrive, can define a function that calculates the payoff. 

Let's create a function called `set_payoffs` under `Group` class in the `models.py`(the name can be anything but this is the name by convention) and let it print something.

```
class Group(BaseGroup):
    average_guess = models.FloatField()

    def set_payoffs(self):
        print('set_payoff works')

```

and then go to `pages.py` to trigger it:

```
class AfterGuessing(WaitPage):
    after_all_players_arrive = 'set_payoffs'
```

We should be able to see the message `set_payoff works` message when all players pass the stage.


````{admonition} Python Break: List comprehension
* List comprehensions allow you to construct a list from a list (or some other iterable) in a single line.

* Very common in Python. 

* The syntax is `[ THING for ITEM in list]`

* For instance:

   ```{code-block} python
   my_list = ['apple', 'banana','pear']

   new_list = [len(i) for i in my_list
   ```
Our new list is: 

   ```{code-block} python
    [5,6,4]
   ```
If we didnt use list comprehension, to produce the same list, we should have done:

```
new_list = []  # Create an empy list
for i in my_list:
    new_list.append(len(i))
```
````
#### Back to `set_payoffs()`

Now that we got the reminder about the list comprehension, lets proceed to build our `set_payoff()` function. This function will be defined in `Groups` class. So `self` refers to the group of the player. So some of the methods we can call are:

* `self_get_players()`
* `self_get_player_by_id(idno)`
* `self_get_player_by_role("rolename")`

We can reach to the parent subsession  by:

* `self.subsession`

Let's define our function and get the players and hold them in a temporary variable called `players`. 

```
def set_payoffs(self):
        players = self.get_players()
```

So players is a list of `player` objects. We can loop over it. We can use list comprehention. We will do both. 

* First we will create `guesses` list by list comprehension
* Then we will calculate the average of it and assign it to our predefined field `average_guess` on `group` object.
* Next we will calculate the distance of the guesses from the average and write to to our predefined field `proximity` on `player` objects
* We will get the minumum proximity 
* We will change the value of `is_winner` on our player objects.
* Finally we will reward the winning person in the same loop by adding up to their built-in `payoff` field.


```
    def set_payoffs(self):
        players = self.get_players()
        guesses = [p.guess for p in players]
        self.average_guess = sum(guesses) / len(guesses)
        
        for p in players:
            p.proximity = abs(p.guess - self.average_guess)

        proximities = [p.proximity for p in players]
        min_proximity = min(proximities)

        for p in players:
            if p.proximity == min_proximity:
                p.is_winner = True
                p.payoff = Constants.reward
```

* We will modify our `Results.html` accordingly.

```
{% extends "global/Page.html" %}
{% load otree static %}

{% block title %}
    Results
{% endblock %}

{% block content %}
The guesses were: 
Your guess was: {{ player.guess }}
The average is: {{ group.average_guess }}

{% if player.is_winner %}
Your guess was the best guess. You win {{ Constants.reward }}
{% else %}
You didn't win. 
{% endif %}

Your payoff is {{ player.payoff }}.

{% endblock %}


```

* We see that it works but we improve it by filters and html tags

```
{% extends "global/Page.html" %}
{% load otree static %}

{% block title %}
    Results
{% endblock %}
<ul>
{% block content %}
  <li>The guesses were: </li>
  <li>Your guess was: {{ player.guess }} </li>
  <li> The average is: {{ group.average_guess | floatformat}} </li>
</ul>

  </li>

{% if player.is_winner %}
Your guess was the best guess.
You win {{ Constants.reward }}
{% else %}
You didn't win. 
{% endif %}
 </br>
Your payoff is {{ player.payoff | c }}.

{% endblock %}


```

* We still miss one final step. We don't have the list of all guesses by players and we cannot call them from our template directly. That's why we should create this list and send it to template.

```{admonition} vars_for_template(self)
We can only use basic loops, conditions and filters in templates and as in the last session we mentioned, every template file have access to methods and attributes of Player, Group, and Constants models (For instance: `{{ player.role }}` , `{{ group.some_variable }}`, `{{ Constants.players_per_group}}` and so on). 

However sometimes we need to access some temporary variables or variables have a higher level of complexity.  If we need to do that, we should send those variables to the template by defining a `vars_for_template(self)` function in the page.

```


So our `Results` page class looks like this:

```
class Results(Page):
    def vars_for_template(self):
        guesses = [p.guess for p in self.group.get_players()]
        return dict(
            guesses=guesses,
        )

```
And we update the `Results.html` as:

```
  <li>The guesses were: {{ guesses }} </li>
```

And here is how it looks:

```{figure} ../figures/guess4.png
---
name: guessingresults
---
Here is how the data looks


