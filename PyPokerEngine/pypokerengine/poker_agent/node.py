import numpy as np

class Node:
    def __init__(self, position, hand, river, betting_amount, player_money, round, k, owner, leaf=False, curr_level=0):
        self.position = position                # Position of the Agent on table (0 or 1)
        self.owner = owner                      # 1 = Poker Agent, 2 = Opposing Player, 3 = Nature
        self.hand = hand                        # Hand of the player
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
        if self.is_leaf:
            return None
        
        
        return None


    def is_leaf(self) -> bool:
        return self.is_leaf
    

    def get_utility(self) -> float:
        if self.is_leaf:
            return self.pot
        return None
    
    
    
    def action_helper_player(self, next, money, k):
       
        is_k = k <= self.curr_level + 1
        next_round = self.round + 1 if next == 3 else self.round
        moves = []

        # Fold State
        moves.append((0, Node(self.position, self.hand, self.river, self.betting_amount, 
                                [self.p1_money, self.p2_money, self.pot], next_round, self.k, next, leaf=True, level=self.curr_level+1)))
        
        # Call State
        if  money >= self.call_amount:
            d1 = self.p1_money - self.call_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.call_amount if self.owner == 2 else self.p2_money
            
            trash = [d1, d2, self.pot + self.call_amount]
            moves.append(1, Node(self.position, self.hand, self.river, self.betting_amount, 
                                    trash, self.round, self.k, next_round, leaf=is_k, level=self.curr_level+1))
        
        # Raise State
        if  money >= self.raise_amount:
            d1 = self.p1_money - self.raise_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.raise_amount if self.owner == 2 else self.p2_money
            
            trash = [d1, d2, self.pot + self.raise_amount]
            moves.append(2, Node(self.position, self.hand, self.river, self.betting_amount, 
                                    trash, self.round, self.k, next_round, leaf=is_k, curr_level=self.curr_level+1))

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