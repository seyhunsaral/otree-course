Advanced Grouping
==================

## Grouping by arrival time `group_by_arrival_time = True`
We can group participants by arrival time by setting the attribute `group_by_arrival_time = True` directly under a `WaitPage`.

    
````{admonition} Things to consider 
* `group_by_arrival_time` is defined on `pages.py` under a page class, unlike previous matching commands.
* `group_by_arrival_time` copies the group structure to future rounds. If a group is rematched, the value is overwritten.
* `group_by_arrival_time` works only if the `WaitPage` is the first page in the app
* You can use `is_displayed` to keep the group structure in the first round only (but every player should see the page)

   ```{code-block} python

    class GroupPage(WaitPage):
        group_by_arrival_time = True

        def is_displayed(self):
            return self.round_number == 1
    ```

* If `group_by_arrival_time = True` all players will be initially in the same group when `creating_session` runs.
* `id_in_group` is not assigned in order participants arrive
* A group's `id_in_subsession` is not necessarily goes from 1 to number of groups. In each grouping a new number is created. 

````
