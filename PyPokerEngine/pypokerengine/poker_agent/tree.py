from node import Node

class Tree:
    def __init__(self, position, hand, river, call_amount, raise_amount, p1Money, p2Money, pot, round, k):
        # bettings = (call_amount, raise_amount)
        # money = (p1Money, p2Money, pot)
        state = {
            "position": position, "hand": hand, "river": river, "call_amount": call_amount, "raise_amount": raise_amount, 
            "p1Money": p1Money, "p2Money": p2Money, "pot": pot, "round": round, "k": k, "owner": 1
            }
        self.root = Node(state)


    # Get the best action to take
    def pick_Action(self) -> int:
        best_action = None # best action
        best_utility = -1 # best utility
        for action, state in self.root.get_actions(): # Pick the action with the highest Utility
            utility = self.get_move_utility(state)
            if utility > best_utility:
                best_action = action
                best_utility = utility
        return best_action

       
    # Get the utility of the move using minmax (without alpha-beta pruning)
    def get_move_utility(self, state, level=0) -> float:
        if state.is_leaf():
            return self.root.get_utility()         
        utils = [self.get_move_utility(nState, level+1) for _, nState in state.get_actions()]
        return max(utils) if level & 1 == 0 else min(utils)

        
        
