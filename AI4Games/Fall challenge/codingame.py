'''
Implemented logic:
    - if possible brew the most valuable potion (only the top one)
    - else:
        - find the cast with the most valuable ingredient you don't have and cast a spell to get it
        - else rest
'''
import sys
import math
from typing import NamedTuple, Dict, Optional, Union, List, Tuple
import numpy as np  # type: ignore
from enum import Enum
from itertools import combinations

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

Spell = NamedTuple('Cast', (
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
    comment: Optional[str] = None

    def __repr__(self):
        s = self.type.name
        if self.id is not None:
            s += f' {self.id}'
        if self.comment is not None:
            s += f' {self.comment}'
        return s


class Agent:

    def __init__(self, max_known_spells: int) -> None:
        self.my_state = State(inventory=np.array([0, 0, 0, 0]), score=0)
        self.opp_state = State(inventory=np.array([0, 0, 0, 0]), score=0)

        self.brew_receipes: Dict[int, Recipe] = {}
        self.spells: Dict[int, Spell] = {}
        self.to_learn: Dict[int, Spell] = {}
        
        self.max_known_spells = max_known_spells


    def get_input(self) -> None:
        self.brew_receipes = {}
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
                self.brew_receipes[action_id] = Recipe(ingredients=deltas, price=price)
            if action_type == 'CAST':
                self.spells[action_id] = Spell(ingredients=deltas, castable=castable, repeatable=repeatable)
            if action_type == 'LEARN':
                self.to_learn[action_id] = Spell(ingredients=deltas, castable=castable, repeatable=repeatable)

        input_values = input().split()
        self.my_state = State(inventory=np.array(list(map(int, input_values[:-1]))), score=int(input_values[-1]))

        input_values = input().split()
        self.opp_state = State(inventory=np.array(list(map(int, input_values[:-1]))), score=int(input_values[-1]))


    def find_action(self) -> Action:
        top_recipe_id, top_recipe = sorted(self.brew_receipes.items(), key=lambda kv: kv[1].price)[-1]
        # for recipe_id, recipe in sorted_recipes:
        if self.can_brew_or_cast(inventory=self.my_state.inventory, recipe_or_spell=top_recipe):
            return Action(type=ActionType.BREW, id=top_recipe_id)
        
        # Learn a cast if less than max_known_spells are known.
        if len(self.spells.items()) < self.max_known_spells:
            return Action(type=ActionType.LEARN, id=list(self.to_learn.items())[0][0])

        # Can't brew any recipes, get ingredients to the most valuable one.
        most_valuable_missing_ingredient = np.nonzero((self.my_state.inventory + top_recipe.ingredients) < 0)[0][-1]

        for ingredient in range(most_valuable_missing_ingredient, -1, -1):
            possible_cast_item = list(
                filter(lambda cast: cast[1].ingredients[ingredient] > 0, self.spells.items())
            )

            if len(possible_cast_item) > 0:
                if self.can_brew_or_cast(self.my_state.inventory, possible_cast_item[0][1]):
                    return Action(
                        type=ActionType.CAST,
                        id=possible_cast_item[0][0],
                        comment=f'missing {most_valuable_missing_ingredient} | will get {ingredient}',
                    )

        return Action(type=ActionType.REST)


    def can_brew_or_cast(self, inventory: np.ndarray, recipe_or_spell: Union[Recipe, Spell]) -> bool:
        if isinstance(recipe_or_spell, Spell) and not recipe_or_spell.castable:
            return False
        
        new_inventory = inventory + recipe_or_spell.ingredients
        return np.all(new_inventory >= 0) and np.sum(new_inventory) <= 10


    def run(self) -> None:
        self.get_input()
        action = self.find_action()
        print(action)


agent = Agent(max_known_spells=10)

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