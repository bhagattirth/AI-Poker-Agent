from pokerAgent.node import Node

class Tree:
    def __init__(self, position, hand, river, call_amount, raise_amount, p1Money, p2Money, pot, round, k, action_history):
        self.position = position                # 0 = Big Blind, 1 = Small Blind
        self.hand = hand                        # Hand of the player
        self.river = river                      # River Cards
        self.CALL_AMOUNT = call_amount          # Amount to call
        self.RAISE_AMOUNT = raise_amount        # Raise Amount
        self.p1 = p1Money                       # Player 1 Money
        self.p2 = p2Money                       # Player 2 Money
        self.pot = pot                          # Pot
        self.round = round                      # Round Number
        self.k = k                              # Game Tree depth
        self.action_history = action_history    # action history
        self.root = Node(position, hand, river, (call_amount, raise_amount), (p1Money, p2Money, pot), round, k, action_history, owner=1) # Current State



    def pick_Action(self) -> int:
        """
        Pick_action returns the best action for a given state based on the utility of the move
        return: returns 0 for fold, 1 for call, 2 for raise
        """ 

        best_action = None                            # best action
        best_utility = float("-inf")                  # best utility
        for action, state in self.root.get_actions(): # Pick the action with the highest Utility
            utility = self.get_move_utility(state)    # Get the utility of the move
            if utility > best_utility:
                best_action = action
                best_utility = utility
        return best_action

       

    def get_move_utility(self, state, level=1) -> float:
        """
        get_move_utility returns the utility of a action using minimax algorithm
        :state: current state of the game (a Node)
        :level: current level of the game tree
        return: returns the utility of the move
        """

        if state.is_leaf_node():    # If the state is a terminal node return the utility of the state
            return state.get_utility()         
        utils = [self.get_move_utility(nState, level+1) for _, nState in state.get_actions()] # Recursively get the utility of future moves
        return max(utils) if level & 1 == 0 else min(utils) # Minmax depending on owner of the node

        
        
