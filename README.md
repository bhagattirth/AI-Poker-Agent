### Set up environment
using the conda or pyenv

- conda create -n CompSci683 python=x.x
- source activate CompSci683

replace the CompSci683 with whatever name you want
replace x.x with the current Python version
https://conda.io/docs/index.html

pip install PyPokerEngine  
https://ishikota.github.io/PyPokerEngine/

pip install numpy
pip install -r requirements.txt

### Files

The required files for the application are run.py and pokeragent.py.

For this application, run.py is the entry point. From here, you can select the number of rounds, the starting stack, the small blind amount, and the competing poker agents. You may run the application through the terminal using the format `python run.py --rounds ROUNDS_INT --stack STACK_INT --i BOOLEAN (CLI player or not)` or may run `python run.py`. Selecting the pokerAgent() in run.py will use a pokerAgent using `pokeragent.py`.


`pokeragent.py` uses the pypokerEngine library to create a poker agent that can be played against other agents.


### pokeragent.py File Structure

`pokeragent.py` has 3 classes: BasePokerPlayer, Tree, and Node.

#### BasePokerPlayer

This class is used to represent a player in pypokerEngine. The most important function in the class is `declare_action(valid_actions, hole_card, round_state)`, where it will decide if it wants to fold, call or raise based on its hold cards and round state. The declare_actions function passes information about the current state of the game into the Tree class where it will use this information to calculate the best move for the agent to take.

### Tree

The Tree picks an action that will maximize the player's utility by analyzing a game tree. Tree is defined by `Tree(position, hand, river, call_amount, raise_amount, p1Money, p2Money, pot, round, k, action_history, raise_count, p2_dist)`, where 'position' is binary with who goes first in a street, 'hand' is the current hand of the agent, `call_amount` and `raise_amount` is the call and raise amounts, `p1Money` and `p2Money` are the agents's and opposing player's stack, `pot` is the current pot size, `round` is the current street, `k` is the depth limit, `action_history`is  the past actions of the agent and opposing player in the game, `raise_count` is the number of raises in the street, and `p2_dist` represents the seen opposing player move distribution over a series of games. Using this information, as well as player1 and player2 hand strengths from `calculate_Hand_Strength()`, it creates Node, which represents the current state (the root). `calculate_Hand_Strength()` takes the input of cards present in the Hand and the River and iterates through the remaining future cards. It calls the function evaluate_cards from the library phevaluator. With the distribution obtained from evaluate_cards, expected hand strength and standard deviation are returned. Similar to PokerMan's card modeling, opponent cards are also modeled, and the opponent's expected hand strength and standard deviation are also returned. 

The Tree class has two functions: `pick_Action` and `get_utility`.

`pick_Action` selects the valid move with the highest utility. Based on the current state, it gets valid all the action-state pairs that can be taken and uses the `get_utility` function to recursively calculate the move's utility using an expectiminimax algorithm. 
`get_utility` goes down to states that are located in level k; if it is a goal node, it returns the pot amount; otherwise, it uses a heuristic to estimate the winnings. The utility is bubbled up, where the agent will choose the utility that maximizes theirs, and the other player will be the min player (the utility is weighted by their move distribution), and nature will return the expectation of the children's utilities.

### Node

Node represents a state in the game tree. Node is defined similarly as mentioned as in the Tree class but contains the hand strength of both players.

The Node Class 6 functions: `has get_actions`, `is_leaf_node`, `get_utility`, `calculate_bluff_probabilty`, `action_helper_player`, and `action_helper_nature`

`is_leaf_node` checks if the current state is a goal node. A state becomes a goal node if an agent chooses to fold, located on level k, or the game ends. 
`has_get_actions` gets the next states based on available actions, `action_helper_player` helps the function get the next state if either player controls the current state, and `action_helper_nature` for nature. 
`get_utility` gets the utility of a goal state. If a goal state results from a Fold Action or the game ends, the utility is the pot. However, for those that have been cut off in level k, a utility is assigned by using a heuristic.`calculate_bluff_probabilty` is used in the heuristic calculation to how often the opposing player bluffs.
