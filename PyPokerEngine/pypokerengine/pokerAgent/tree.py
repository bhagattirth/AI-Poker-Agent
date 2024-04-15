from pypokerengine.pokerAgent.node import Node

class Tree:
    def __init__(self, position, hand, river, call_amount, raise_amount, p1Money, p2Money, pot, round, k):
        self.position = position         # 0 = Big Blind, 1 = Small Blind
        self.hand = hand                 # Hand of the player
        self.river = river               # River Cards
        self.CALL_AMOUNT = call_amount   # Amount to call
        self.RAISE_AMOUNT = raise_amount # Raise Amount
        self.p1 = p1Money                # Player 1 Money
        self.p2 = p2Money                # Player 2 Money
        self.pot = pot                   # Pot
        self.round = round               # Round Number
        self.k = k                       # Game Tree depth
        self.root = Node(position, hand, river, (call_amount, raise_amount), (p1Money, p2Money, pot), round, k, owner=1)


    # Get the best action to take
    def pick_Action(self) -> int:
        best_action = None # best action
        best_utility = float("-inf") # best utility
        for action, state in self.root.get_actions(): # Pick the action with the highest Utility
            utility = self.get_move_utility(state)
            if utility > best_utility:
                best_action = action
                best_utility = utility
        return best_action

       
    # Get the utility of the move using minmax (without alpha-beta pruning)
    def get_move_utility(self, state, level=1) -> float:
        if state.is_leaf_node():
            return state.get_utility()         
        utils = [self.get_move_utility(nState, level+1) for _, nState in state.get_actions()]
        if state.owner == 3:
            return max(utils) if (level+1) & 1 == 0 else min(utils)
        return max(utils) if level & 1 == 0 else min(utils)

        
        
