### Fall challenge, Jakub Grodzicki

I created a bot in Python. 

#### First approach
My first simple approach to get out of the `Wood` was based on a greedy algorithm.

Idea:
- if possible - brew any potion
- find a spell giving the most valuable ingredient I don't have, that's required for the potion with the biggest price
- rest if no spells are available

It was simple, but it worked so I was in the `Bronze`.

#### Second approach
Idea:
- at first learn some spells
    - no heuristic to determine the best one
    - learn the first one, not to spend money on that
    - goal: learn 7 new spells
- then for each move run a BFS
    - no special logic here
    - expand the action tree only if I can cast the spell (also check if spell is repeatable)
    - goal: run till I don't find a first potion I can brew
- if I didn't find a potion to brew in given time - cast a random spell

I tried also running the BFS until the most valuable potion was brewable, but usually I wasn't able to do so, ending up 
doing a random move.

#### Final results
Second approach was enough for the place no `1196`. 

#### Contribution on the forum
https://forum.codingame.com/t/fall-challenge-2020-feedbacks-strategies/187846/126?u=notojapko