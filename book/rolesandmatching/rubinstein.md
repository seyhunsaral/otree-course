(rubinstein-bargaining)=
Practice: Rubinstein Bargaining Game
=====================================

We will create a Rubinstein Bargaining Game with follwing properties:

* The pie to bargain on: 100 ECU
* Two players: One proposes, one accepts/rejects
* If the responder accept the proposal, they recieve the relevant amount. If not in the next round:
  * They swith roles
  * The pie dimnishes by 25 ECU
* If there is no agreement, the game stops after the 4th round. (When the total pie is over)

* In our game we will have two separate games. The players play the game twice with different partners.


# Planning the game


<!--
```{figure} ../figures/trust_game_str.png
---
name: trust_game_str
---
Trust Game Structure
```
-->
| Page         | Description                                      |
|--------------|--------------------------------------------------|
| MatchInfo    | Display informaiton about matching               |
| Offer        | Proposer offers an amout between `0` and `100`   |
| WaitOffer    | Responder waits                                  |
| Response     | Responder accepts or rejects the offer           |
| WaitResponse | Proposer waits                                   |
| Results      | They will both see whether it is accepted or not |
| FinalResults | They will see the final payoffs                  |


