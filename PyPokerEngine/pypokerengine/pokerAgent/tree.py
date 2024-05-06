from .node import Node, calculate_hand_strength

class Tree:
    def __init__(self, position, hand, river, call_amount, raise_amount, p1Money, p2Money, pot, round, k, action_history, raise_count=0, p2_dist=[1,1,1]):
        self.round = round                      

        p1_hand_strength, p2_hand_strength, p1_hand_strength_rmse, p2_hand_strength_rmse = calculate_hand_strength(hand, river) # Note: hand will always be our (player 1's) cards
        self.root = Node(
            position=position,
            hand=hand,
            river=river,
            betting_amount=(call_amount, raise_amount),
            player_money=(p1Money, p2Money, pot),
            round=round,
            k=k,
            action_history=action_history,
            owner=1,
            action=action_history[-1][1],
            raise_count=raise_count,
            p1_hand_strength=p1_hand_strength,
            p2_hand_strength=p2_hand_strength,
            p1_hand_strength_rmse=p1_hand_strength_rmse,
            p2_hand_strength_rmse=p2_hand_strength_rmse,
            p2_dist=p2_dist
        ) # Current State


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
        is_preflop = self.round == 1
        # print(state.weight)
        if state.is_leaf_node():    # If the state is a terminal node return the utility of the state
            return state.get_utility(is_preflop=is_preflop)

        actions = state.get_actions(is_preflop=is_preflop)

        if not actions:
            return state.get_utility(is_preflop=is_preflop)


        utils = [nState.weight * self.get_move_utility(nState, level+1) for _, nState in actions] # Recursively get the utility of future moves
        

        if state.owner == 1:
            return max(utils)
        elif state.owner == 2:
            return sum(utils)/len(utils)
        else:
            return sum(utils)/len(utils)



