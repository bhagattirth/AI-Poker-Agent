from itertools import combinations
import time
from phevaluator.evaluator import evaluate_cards
import numpy as np

def calculate_hand_strength(hand, river):
    # Given hand cards ('hand', 2 cards) and community cards ('river', up to 5 cards)
    # Determine the holder's hand strength
    start_time=time.time()
    all_cards = ['C2', 'D2', 'H2', 'S2', 'C3', 'D3', 'H3', 'S3', 
                        'C4', 'D4', 'H4', 'S4', 'C5', 'D5', 'H5', 'S5', 
                        'C6', 'D6', 'H6', 'S6', 'C7', 'D7', 'H7', 'S7',
                        'C8', 'D8', 'H8', 'S8', 'C9', 'D9', 'H9', 'S9', 
                        'CT', 'DT', 'HT', 'ST', 'CJ', 'DJ', 'HJ', 'SJ',
                        'CQ', 'DQ', 'HQ', 'SQ', 'CK', 'DK', 'HK', 'SK', 
                        'CA', 'DA', 'HA', 'SA']
    card_eval={}
    opp_eval={}
    for card in hand:
        all_cards.remove(card)

    for card in river:
        all_cards.remove(card)

    if river==[]: #Computing hand values for preflop round
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                for k in range(j+1,len(all_cards)):
                    card_value=evaluate_cards(hand[0][::-1],hand[1][::-1], all_cards[i][::-1], all_cards[j][::-1], all_cards[k][::-1])
                    card_eval[card_value]=card_eval.get(card_value,0)+1
    elif len(river)==3:
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                opp_value=evaluate_cards(river[0][::-1],river[1][::-1],river[2][::-1],all_cards[i][::-1],all_cards[j][::-1])
                opp_eval[opp_value]=opp_eval.get(opp_value,0)+1
        card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1])
        card_eval[card_value]=card_eval.get(card_value,0)+1
    elif len(river)==4:
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                opp_value=evaluate_cards(river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],all_cards[i][::-1],all_cards[j][::-1])
                opp_eval[opp_value]=opp_eval.get(opp_value,0)+1
        card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1])
        card_eval[card_value]=card_eval.get(card_value,0)+1
    elif len(river)==5:
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                    opp_value=evaluate_cards(river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],river[4][::-1],all_cards[i][::-1],all_cards[j][::-1])
                    opp_eval[opp_value]=opp_eval.get(opp_value,0)+1
        card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],river[4][::-1])
        card_eval[card_value]=card_eval.get(card_value,0)+1

    # PokerMan Value calculation
    value=0
    for i,v in card_eval.items():
        value=value+(i*v)
    if len(card_eval)>0:value=value/sum(card_eval.values())
    value=(7462-value)/7462 

    # PokerMan Variance Calculation:
    variance=0
    for i,v in card_eval.items():
        i_norm=(7462-i)/7462 
        variance= (np.power(i_norm-value,2)*v)+variance
    variance=np.sqrt(variance)
    if len(card_eval)>0:variance=variance/sum(card_eval.values())


    # Opponent Value Calculation:
    opp_value=0
    for i,v in opp_eval.items():
        opp_value=opp_value+(i*v)
    if len(opp_eval)>0:opp_value=opp_value/sum(opp_eval.values())
    opp_value=(7462-opp_value)/7462 

    # Opponent Variance Calculation:
    opp_variance=0
    for i,v in opp_eval.items():
        i_norm=(7462-i)/7462 
        opp_variance= (np.power(i_norm-opp_value,2)*v)+opp_variance
    opp_variance=np.sqrt(opp_variance)
    if len(opp_eval)>0:opp_variance=opp_variance/sum(opp_eval.values())
    return value, opp_value, variance, opp_variance  
 
class Node:
    def __init__(self, position, hand, river, betting_amount, player_money, round, k, action_history,owner, action, aggression=0, leaf=False, curr_level=0):
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
        self.round = round                      # Current Round
        self.k = k                              # Number of cards to draw
        self.is_leaf = leaf                     # Is this a leaf node?
        self.curr_level = curr_level            # Current level of the tree
        self.action_history = action_history    # Action History
        self.action = action                    # Action which led to this node {'CALL', 'RAISE', 'FOLD', 'NATURE', 'SMALLBLIND', 'BIGBLIND'}
        self.aggression = aggression            # How aggressively is player 2 playing?


    def get_actions(self, is_preflop=False) -> list:
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

        if is_preflop:
            return None

        if self.owner == 3 and self.position == 0:            # Natures Turn and next player is the pokeragent
            return self.action_helper_nature(2)
        else:
            return self.action_helper_nature(1)                 # Natures Turn and next player is the opponent


    def is_leaf_node(self) -> bool:
        """
        is_leaf_node returns if the current node is a leaf node
        return: returns a boolean value
        """
        return self.is_leaf


    def get_utility(self, is_preflop=False) -> float:
        """
        get_utility returns the utility of the current node
        return: returns the current pot (temporary)
        """
        p1_bet_amount = sum([play[2] for play in self.action_history if play[0] == 1])
        p2_bet_amount = sum([play[2] for play in self.action_history if play[0] == 2])

        # If we fold, we will lose all that we've bet.
        if self.owner == 1 and self.action == 'FOLD':
            return -1 * p1_bet_amount

        # If they fold, we will win the pot.
        if self.owner == 2 and self.action == 'FOLD':
            return self.pot

        # If nature controlled node, report max possible winnings
        if self.owner == 3:
            return self.pot
        
        hand_strength,opp_hand_strength, variance,opp_variance= calculate_hand_strength( self.hand, self.river) # Note: hand will always be our (player 1's) cards

        # If preflop, expect to win the hand
        if is_preflop:
            return self.pot

        # TODO: Account for p2 predicted expected hand strength
        # TODO: Account for bluffing
        # TODO: Account for aggression
        # TODO: Account for past results
        feels_like_a_weaker_hand = abs(hand_strength-opp_hand_strength) < 0.5
        print(feels_like_a_weaker_hand,hand_strength)

        # If we feel that our hand is weaker, we expect to lose all that we've bet so far.
        if feels_like_a_weaker_hand:
            return -1 * p1_bet_amount

        # In all other cases, we expect to win the pot
        return self.pot

    def calculate_bluff_probability(self):
        """
        calculate_bluff_probability returns the probability of the opponent bluffing throughout the game
        return: returns the value of opp_bluff_prob 
        """
        opp_bluff_prob = 0
        hand_strength = calculate_hand_strength(self.hand, self.river)
        pred_p2_hand_strength = 0 # TODO: account for p2 predicted expected hand strength; i believe abstraction will be needed in this step.
        if self.p1_money < self.p2_money:
            opp_bluff_prob += 0.1
        if hand_strength < pred_p2_hand_strength:
            opp_bluff_prob += 0.1
        return opp_bluff_prob
    
    def opp_aggression(self):
        """
        opp_aggression accounts how aggressively the opponent is playing/betting throughout the game
        return: returns the value of self.aggression 
        """
        # TODO: added this attribute everywhere when initializing a node in order to keep track throughout the games, 
        # TODO: but the initialization might need to be fixed to prevent potential bugs of always being set to 0.
        # TODO: if self.aggression is always 0 (bug), look at pokeragent.py, node.py, and tree.py.
        prev_action = None
        if len(self.action_history) > 0:
            prev_action = self.action_history[-1][1]
        # TODO: need to optimize values more appropriately for self.aggression based on the actions and how it ties to main heuristic.
        # TODO: do we want the range from [0, 1] or [0, inf)?
        if prev_action == 'RAISE':
            self.aggression += 1
        elif prev_action == 'CALL':
            self.aggression += 0.5
        elif prev_action == 'FOLD':
            self.aggression -= 1
            if self.aggression < 0:
                self.aggression = 0
        else:
            self.aggression = 0
        return self.aggression

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
        moves.append((0, Node(
            position=self.position,
            hand=self.hand,
            river=self.river,
            betting_amount=self.betting_amount,
            player_money=[self.p1_money, self.p2_money, self.pot],
            round=next_round,
            k=self.k,
            action_history=[*self.action_history, (self.owner, 'FOLD', 0.0)],
            owner=self.owner,
            leaf=True,
            curr_level=self.curr_level+1,
            action='FOLD',
        )))

        # Call State
        if  money >= self.call_amount:
            # Update the money of the player after calling
            d1 = self.p1_money - self.call_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.call_amount if self.owner == 2 else self.p2_money
            new_amounts = (0, 10) # Update the betting amounts

            moves.append((1, Node(
                position=self.position,
                hand=self.hand,
                river=self.river,
                betting_amount=new_amounts,
                player_money=[d1, d2, self.pot + self.call_amount],
                round=next_round,
                k=self.k,
                action_history=[*self.action_history, (self.owner, 'CALL', self.call_amount)],
                owner=next,
                leaf=is_k,
                curr_level=self.curr_level+1,
                action='CALL',
            )))

        # Raise State
        if  money >= self.raise_amount :
            # Update the money of the player after raising
            d1 = self.p1_money - self.raise_amount  if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.raise_amount if self.owner == 2 else self.p2_money

            new_amounts = (10, 20) #updating the betting amounts
            moves.append((2, Node(
                position=self.position,
                hand=self.hand,
                river=self.river,
                betting_amount=new_amounts,
                player_money=[d1, d2, self.pot + self.raise_amount],
                round=next_round,
                k=self.k,
                action_history=[*self.action_history, (self.owner, 'RAISE', self.raise_amount)],
                owner=next,
                leaf=is_k,
                curr_level=self.curr_level+1,
                action='RAISE',
                
            )))

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

        # Remaining cards Choose 3 cards states
        if num_cards == 3:
            valid_combinations = list(combinations(remaining_cards, num_cards))
            moves = [(-1, Node(
                position=self.position,
                hand=self.hand,
                river=list(branch),
                betting_amount=self.betting_amount,
                player_money=[self.p1_money, self.p2_money, self.pot],
                round=self.round,
                k=self.k,
                action_history=[*self.action_history],
                owner=next,
                leaf=is_k,
                curr_level=self.curr_level+1,
                action='NATURE',
            ))for branch in valid_combinations]

        else:
            moves = [(-1, Node(
                position=self.position,
                hand=self.hand,
                river=self.river + [card],
                betting_amount=self.betting_amount,
                player_money=[self.p1_money, self.p2_money, self.pot],
                round=self.round,
                k=self.k,
                action_history=[*self.action_history],
                owner=next,
                leaf=is_k,
                curr_level=self.curr_level+1,
                action='NATURE',
            ))for card in remaining_cards]

        return moves
