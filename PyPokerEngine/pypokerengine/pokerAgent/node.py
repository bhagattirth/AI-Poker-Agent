# import numpy as np
from itertools import combinations

class Node:
    def __init__(self, position, hand, river, betting_amount, player_money, round, k, owner, leaf=False, curr_level=0):
        self.position = position                # If the agent is the First Player or Second Player (0 or 1)
        self.owner = owner                      # 1 = Poker Agent, 2 = Opposing Player, 3 = Nature
        self.hand = hand                        # Hand of the Agent
        self.river = river                      # River Cards
        self.betting_amount = betting_amount    # Amount to call and raise
        self.call_amount = betting_amount[0]    # Amount to call
        self.raise_amount = betting_amount[1]   # Amount to raise
        self.p1_money = player_money[0]         # Money of the player 1
        self.p2_money = player_money[1]         # Money of the player 2
        self.pot = player_money[2]              # Pot
        self.round = round                      # current Round
        self.k = k                              # Number of cards to draw
        self.is_leaf = leaf                     # Is this a leaf node
        self.curr_level = curr_level            # Current level of the tree


    def get_actions(self) -> list:
        """
        get_actions returns the possible actions the player can take
        return: returns a list of states from valid actions
        """

        if self.is_leaf: # There are no actions at a termimal node
            return None
        
        if self.owner == 1 and self.position == 0:              # If the pokeragent plays first
            return self.action_helper_player(2, self.p1_money)  
        elif self.owner == 1 and self.position == 1:            # If the pokeragent plays second
            return self.action_helper_player(3, self.p1_money)
        elif self.owner == 2 and self.position == 0:            # If the opponent plays first
            return self.action_helper_player(3, self.p2_money)
        elif self.owner == 2 and self.position == 1:            # If the opponent plays second
            return self.action_helper_player(1, self.p2_money)
        elif self.owner == 3 and self.position == 0:            # Natures Turn and next player is the pokeragent
            return self.action_helper_nature(2)
        else:
            return self.action_helper_nature(1)                 # Natures Turn and next player is the opponent
        

    def is_leaf_node(self) -> bool: 
        """
        is_leaf_node returns if the current node is a leaf node
        return: returns a boolean value
        """
        return self.is_leaf
    

    def get_utility(self) -> float:
        """
        get_utility returns the utility of the current node
        return: returns the current pot (temporary)
        """
        if self.is_leaf:
            return self.pot * (-1 if self.owner == 1 else 1)
        return None
    
    
    
    def action_helper_player(self, next, money):
        """
        action_helper_player returns valid states for the player
        :next: next player
        :money: money of the player
        return: returns a list of states from valid actions
        """


        next_round = self.round + 1 if next == 3 else self.round # Check if taking an action leads to the next round
        is_k = self.k <= self.curr_level + 1 or next_round == 5  # Check if the depth limit is reached or the game is over
        moves = [] # List of valid states

        # Fold State
        moves.append((0, Node(self.position, self.hand, self.river, self.betting_amount, 
                                [self.p1_money, self.p2_money, self.pot], next_round, self.k, self.owner, leaf=True, curr_level=self.curr_level+1)))
        
        # Call State
        if  money >= self.call_amount:
            # Update the money of the player after calling
            d1 = self.p1_money - self.call_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.call_amount if self.owner == 2 else self.p2_money
            new_amounts = (0, 10) # Update the betting amounts

            trash = [d1, d2, self.pot + self.call_amount]
            moves.append((1, Node(self.position, self.hand, self.river, new_amounts, 
                                    trash, next_round, self.k, next, leaf=is_k, curr_level=self.curr_level+1)))
        
        # Raise State
        if  money >= self.raise_amount :
            # Update the money of the player after raising
            d1 = self.p1_money - self.raise_amount  if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.raise_amount if self.owner == 2 else self.p2_money
            
            trash = [d1, d2, self.pot + self.raise_amount]
            new_amounts = (10, 20) #updating the betting amounts
            moves.append((2, Node(self.position, self.hand, self.river, self.betting_amount, 
                                    trash, next_round, self.k, next, leaf=is_k, curr_level=self.curr_level+1)))

        return moves

    
    
    def action_helper_nature(self, next):
        """
        action_helper_nature returns valid states for nature
        :next: next player
        return: returns a list of states from valid actions
        """
        self.owner = 1 if self.position == 0 else 2
        is_k = self.k <= self.curr_level + 1    # Checks if the depth limit is reached
        num_cards = 3 if self.round == 2 else 1 # Number of cards to show on the river

        all_cards = ['C2', 'D2', 'H2', 'S2', 'C3', 'D3', 'H3', 'S3', 
                     'C4', 'D4', 'H4', 'S4', 'C5', 'D5', 'H5', 'S5', 
                     'C6', 'D6', 'H6', 'S6', 'C7', 'D7', 'H7', 'S7',
                     'C8', 'D8', 'H8', 'S8', 'C9', 'D9', 'H9', 'S9', 
                     'CT', 'DT', 'HT', 'ST', 'CJ', 'DJ', 'HJ', 'SJ',
                     'CQ', 'DQ', 'HQ', 'SQ', 'CK', 'DK', 'HK', 'SK', 
                     'CA', 'DA', 'HA', 'SA']

        remaining_cards = [card for card in all_cards if card not in self.hand and card not in self.river] # Remaining cards that are not on hand or river

        # Remainng cards Choose 3 cards states
        if num_cards == 3:
            valid_combinations = list(combinations(remaining_cards, num_cards))
            moves = [(-1, Node(self.position, self.hand, list(branch), self.betting_amount, [self.p1_money, self.p2_money, self.pot],
                                self.round, self.k, next, leaf=is_k, curr_level=self.curr_level+1)) for branch in valid_combinations]

        else:
            moves = [(-1, Node(self.position, self.hand, self.river + [card], self.betting_amount, [self.p1_money, self.p2_money, self.pot],
                                self.round, self.k, next, leaf=is_k, curr_level=self.curr_level+1)) for card in remaining_cards]

        return moves
        


































# class Node:
#     def __init__(self, parent = None, action = None, owner = None) -> None:
#         self.parent = parent
#         self.action = action # action which caused the player to transition from parent to action. None indicates root node
#         self.owner = owner # which entity controls this node (P1, P2, etc.)
#         self.children = np.array([], dtype='object')
#         self 
    
#     def __repr__(self) -> str:
#         return "<[Node] Owner: {} parent: {}>".format(self.owner, self.parent)

    
# class LeafNode(Node):
#     def __init__(self, parent = None, action = None, owner = None, utility = None):
#         super(parent=parent, action=action, owner=owner)
#         self.utility = utility

#     def calc_utility(self):
#         return None