'''
Implemented logic:
    - for fixed amount of rounds learn new spells
    
    - if possible brew the most valuable potion (or any - depending on the parametere)
    - else:
        - run a BFS to find which spell to cast for the fastest way of getting to brewing a potion (most val. or any)
'''
from collections import deque
import sys
import math
from typing import NamedTuple, Dict, Optional, Union, List, Tuple, Deque
import numpy as np  # type: ignore
from enum import Enum
from itertools import combinations
import time

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


def log(msg):
    print(msg, file=sys.stderr, flush=True)


class State(NamedTuple('State', (
    ('inventory', np.ndarray),
    ('score', int),
))):
    def __copy__(self):
        return State(inventory=self.inventory.copy(), score=self.score)


Recipe = NamedTuple('Recipe', (
    ('ingredients', np.ndarray),
    ('price', int),
))

Spell = NamedTuple('Spell', (
    ('ingredients', np.ndarray),
    ('castable', bool),
    ('repeatable', bool),
))


class ActionType(Enum):
    BREW = 'BREW'
    CAST = 'CAST'
    REST = 'REST'
    WAIT = 'WAIT'
    LEARN = 'LEARN'


class Action(NamedTuple):
    type: ActionType
    id: Optional[int] = None
    times_used: Optional[int] = None
    comment: Optional[str] = None

    def __repr__(self):
        s = self.type.name
        if self.id is not None:
            s += f' {self.id}'
        if self.times_used is not None:
            s += f' {self.times_used}'
        if self.comment is not None:
            s += f' {self.comment}'
        return s


class Agent:

    def __init__(self, max_known_spells: int, go_for_most_valuable: bool) -> None:
        self.my_state = State(inventory=np.array([0, 0, 0, 0]), score=0)
        self.opp_state = State(inventory=np.array([0, 0, 0, 0]), score=0)

        self.brew_recipes: Dict[int, Recipe] = {}
        self.spells: Dict[int, Spell] = {}
        self.to_learn: Dict[int, Spell] = {}
        
        self.max_known_spells = max_known_spells
        self.go_for_most_valuable = go_for_most_valuable


    def get_input(self) -> None:
        self.brew_recipes = {}
        self.spells = {}
        self.to_learn = {}

        action_count = int(input())
        for _ in range(action_count):
            input_values = input().split()
            action_id, action_type = int(input_values[0]), input_values[1]
            deltas = list(map(int, input_values[2:6]))
            deltas = np.array(deltas)
            price = int(input_values[6])
            tome_index, tax_count = map(int, input_values[7:9])
            castable, repeatable = map(lambda s: s != '0', input_values[9:11])

            if action_type == 'BREW':
                self.brew_recipes[action_id] = Recipe(ingredients=deltas, price=price)
            if action_type == 'CAST':
                self.spells[action_id] = Spell(ingredients=deltas, castable=castable, repeatable=repeatable)
            if action_type == 'LEARN':
                self.to_learn[action_id] = Spell(ingredients=deltas, castable=castable, repeatable=repeatable)

        input_values = input().split()
        self.my_state = State(inventory=np.array(list(map(int, input_values[:-1]))), score=int(input_values[-1]))

        input_values = input().split()
        self.opp_state = State(inventory=np.array(list(map(int, input_values[:-1]))), score=int(input_values[-1]))


    def find_action(self) -> Action:
        if self.go_for_most_valuable:
            top_recipe_id, top_recipe = sorted(self.brew_recipes.items(), key=lambda kv: kv[1].price)[-1]
            
            if self.can_brew_or_cast(inventory=self.my_state.inventory, recipe_or_spell=top_recipe):
                return Action(type=ActionType.BREW, id=top_recipe_id)
        else:
            for id, brew_recipe in sorted(self.brew_recipes.items(), key=lambda kv: kv[1].price, reverse=True):
                if self.can_brew_or_cast(inventory=self.my_state.inventory, recipe_or_spell=brew_recipe):
                    return Action(type=ActionType.BREW, id=id)
        
        # Learn a cast if less than max_known_spells are known.
        if len(self.spells.items()) < self.max_known_spells:
            return Action(type=ActionType.LEARN, id=list(self.to_learn.items())[0][0])
        
        action = self.BFS()
        
        if action is None:
            castable_spells = list(filter(
                lambda kv: kv[1].castable and
                           self.can_brew_or_cast(inventory=self.my_state.inventory, recipe_or_spell=kv[1]),
                self.spells.items()
            ))
            if len(castable_spells) > 0:
                return Action(type=ActionType.CAST, id=castable_spells[0][0], comment='random cast')
            else:
                return Action(type=ActionType.REST, comment='jednak chillera')
        return action


    def can_brew_or_cast(self, inventory: np.ndarray, recipe_or_spell: Union[Recipe, Spell]) -> bool:
        if isinstance(recipe_or_spell, Spell) and not recipe_or_spell.castable:
            return False
        
        new_inventory = inventory + recipe_or_spell.ingredients
        return np.all(new_inventory >= 0) and np.sum(new_inventory) <= 10
    
    
    def BFS(self) -> Optional[Action]:
        '''
        :param find_to_first: try to brew the first possible potion, if false will go for the most valuable one
        :return: first move to get to obtain the inventory to be able to brew a potion
        '''
        q: Deque = deque()
        q.append((self.my_state.inventory.copy(), self.spells.copy(), None))
        
        brew_recipes_ingredients = np.array([recipe.ingredients for recipe in self.brew_recipes.values()])
        brew_recipes_prices = [recipe.price for recipe in self.brew_recipes.values()]
        best_brew_recipe = list(self.brew_recipes.values())[np.argmax(brew_recipes_prices)]
        
        st_time = time.time()

        cnt = 0
        while len(q) > 0 and time.time() - st_time < 0.04:
            cnt += 1
            log(cnt)
            
            inventory, spells, first_action = q.popleft()
            
            # CAST a spell
            for id, spell in spells.items():
                if spell.castable and self.can_brew_or_cast(inventory=inventory, recipe_or_spell=spell):
                    new_inventory = inventory.copy()
                    new_inventory += spell.ingredients

                    can_brew = np.all(new_inventory + brew_recipes_ingredients >= 0, axis=1)

                    if self.go_for_most_valuable and self.can_brew_or_cast(new_inventory, best_brew_recipe):
                        return first_action if first_action is not None \
                            else Action(ActionType.CAST, id=id)
                    elif not self.go_for_most_valuable and any(can_brew):
                        return first_action if first_action is not None \
                            else Action(ActionType.CAST, id=id)
                    
                    q.append((
                        new_inventory,
                        self._spells_after_cast(spells=spells, cast_id=id),
                        first_action if first_action is not None else Action(type=ActionType.CAST, id=id, times_used=1),
                    ))
                    
                    if spell.repeatable:
                        times_used = 2
                        while self.can_brew_or_cast(inventory=new_inventory, recipe_or_spell=spell):
                            new_inventory += spell.ingredients
                            can_brew = np.all(new_inventory >= brew_recipes_ingredients, axis=1)

                            if self.go_for_most_valuable and self.can_brew_or_cast(new_inventory, best_brew_recipe):
                                return first_action if first_action is not None \
                                    else Action(ActionType.CAST, id=id, times_used=times_used)
                            elif not self.go_for_most_valuable and any(can_brew):
                                return first_action if first_action is not None \
                                    else Action(ActionType.CAST, id=id, times_used=times_used)
                                
                            q.append((
                                new_inventory,
                                self._spells_after_cast(spells=spells, cast_id=id),
                                first_action if first_action is not None else Action(
                                    type=ActionType.CAST,
                                    id=id,
                                    times_used=times_used,
                                ),
                            ))
                            times_used += 1
            # REST
            q.append((
                inventory,
                self._spells_after_rest(spells=spells),
                first_action if first_action is not None else Action(type=ActionType.REST),
            ))
        return None
        
    def _spells_after_rest(self, spells: Dict[int, Spell]) -> Dict[int, Spell]:
        new_spells = {}
        for id, spell in spells.items():
            new_spells[id] = Spell(ingredients=spell.ingredients, castable=True, repeatable=spell.repeatable)
        return new_spells
    
    
    def _spells_after_cast(self, spells: Dict[int, Spell], cast_id: int) -> Dict[int, Spell]:
        new_spells = {}
        for id, spell in spells.items():
            new_spells[id] = Spell(
                ingredients=spell.ingredients,
                castable=spell.castable if id != cast_id else False,
                repeatable=spell.repeatable,
            )
        return new_spells
    

    def run(self) -> None:
        self.get_input()
        action = self.find_action()
        print(action)


agent = Agent(max_known_spells=10, go_for_most_valuable=False)

while True:
    agent.run()

    # action_id: the unique ID of this spell or recipe
    # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
    # delta_0: tier-0 ingredient change
    # delta_1: tier-1 ingredient change
    # delta_2: tier-2 ingredient change
    # delta_3: tier-3 ingredient change
    # price: the price in rupees if this is a potion
    # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
    # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
    # castable: in the first league: always 0; later: 1 if this is a castable player spell
    # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell


    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT1