from itertools import combinations
import time
from phevaluator.evaluator import evaluate_cards
import numpy as np
from math import inf

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
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1],all_cards[i][::-1],all_cards[j][::-1])
                card_eval[card_value]=card_eval.get(card_value,0)+1
       
    elif len(river)==4:
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                opp_value=evaluate_cards(river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],all_cards[i][::-1],all_cards[j][::-1])
                opp_eval[opp_value]=opp_eval.get(opp_value,0)+1
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],all_cards[i][::-1])
                card_eval[card_value]=card_eval.get(card_value,0)+1
    elif len(river)==5:
        for i in range(len(all_cards)):
            for j in range(i+1,len(all_cards)):
                    opp_value=evaluate_cards(river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],river[4][::-1],all_cards[i][::-1],all_cards[j][::-1])
                    opp_eval[opp_value]=opp_eval.get(opp_value,0)+1
        card_value=evaluate_cards(hand[0][::-1],hand[1][::-1],river[0][::-1],river[1][::-1],river[2][::-1],river[3][::-1],river[4][::-1])
        card_eval[card_value]=card_eval.get(card_value,0)+1

    max_theoretical_hand_strength = 7462
    # PokerMan Value calculation
    value=0
    for i,v in card_eval.items():
        value=value+(i*v) # cumulative sum of hand strength values
    if len(card_eval)>0:value=value/sum(card_eval.values()) # calculating mean hand strength
    value=(max_theoretical_hand_strength-value)/max_theoretical_hand_strength # normalizing mean hand strength (NOTE: for PHE - lower score is stronger hand, so flipping relationship here)

    # PokerMan Variance Calculation:
    variance=0
    for i,v in card_eval.items():
        i_norm=(max_theoretical_hand_strength-i)/max_theoretical_hand_strength # (NOTE: for PHE - lower score is stronger hand, so flipping relationship here)
        variance= (np.power(i_norm-value,2)*v)+variance
    std_dev=np.sqrt(variance)
    if len(card_eval)>0:std_dev=std_dev/sum(card_eval.values())


    # Opponent Value Calculation:
    opp_value=0
    for i,v in opp_eval.items():
        opp_value=opp_value+(i*v)
    if len(opp_eval)>0:opp_value=opp_value/sum(opp_eval.values()) # calculating mean hand strength
    opp_value=(max_theoretical_hand_strength-opp_value)/max_theoretical_hand_strength # normalizing mean hand strength (NOTE: for PHE - lower score is stronger hand, so flipping relationship here)

    # Opponent Variance Calculation:
    opp_variance=0
    for i,v in opp_eval.items():
        i_norm=(max_theoretical_hand_strength-i)/max_theoretical_hand_strength # (NOTE: for PHE - lower score is stronger hand, so flipping relationship here)
        opp_variance= (np.power(i_norm-opp_value,2)*v)+opp_variance
    opp_std_dev=np.sqrt(opp_variance)
    if len(opp_eval)>0:opp_std_dev=opp_std_dev/sum(opp_eval.values())
    return value, opp_value, std_dev, opp_std_dev

def determine_victory(params, risk_level='high'):
    # TODO: Account for bluffing
    # TODO: Account for past results

    hypers = {}
    # critical val: determines confidence levels and is expressed as overlap between possible hand values between us and them. higher is more unlikely, 0 is exact values (mean/calc)
    # betting power threshold: an exponential curve from (-inf, 1) where 0 => equal wealth, 1 => complete monopoly, -inf => bankruptcy
    # round_raise_threshold: how many raises do we want to tolerate from usual (us + their raises, cumulative in this round)

    hypers['zero'] = {
        'critical_val': 1, # tuned from 2 to 0.5 for a relatively tight interval where the overlap between the hands' values is minimal 
        'betting_power_threshold': -inf, # ideally, we can tolerate being bankrupt if we know we will be winning this hand
        'round_raise_threshold': inf, # ideally, we can tolerate any number of raises if we know we will be winning this hand
    }

    hypers['low'] = {
        'critical_val': 0.33, # tuned from 1 to 0.25 for a slightly wider confidence interval, indicating low, yet meaningful risk
        'betting_power_threshold': -100,
        'round_raise_threshold': 5,
    }

    hypers['med'] = {
        'critical_val': 0.25, # tuned from 0.5 to 0.15 for a medium-level risk, creating a broader sense of the confidence interval
        'betting_power_threshold': 0, # we should have as much money as them to risk this
        'round_raise_threshold': 3, # Or we must not stand to lose a lot of money to risk this
    }

    hypers['high'] = {
        'critical_val': 0.1, # tuned from 0.25 to 0.1 to signify high risk and the large range of different outcomes
        'betting_power_threshold': 0.5, # only risk it if we can afford to lose
        'round_raise_threshold': 0, # only risk it if there hasn't been a raise in this round (when we cannot afford to lose)
    }

    p1_hand_strength_lower_bound = params['hand_info']['p1_hand_strength'] - hypers[risk_level]['critical_val'] * params['hand_info']['p1_hand_strength_rmse']
    p2_hand_strength_upper_bound = params['hand_info']['p2_hand_strength'] + hypers[risk_level]['critical_val'] * params['hand_info']['p2_hand_strength_rmse']
    return (
            p1_hand_strength_lower_bound > p2_hand_strength_upper_bound
            and (
                params['relative_betting_power'] >= hypers[risk_level]['betting_power_threshold'] # either be above a comfortable wealth disparity level
                or params['num_round_raises'] <= hypers[risk_level]['round_raise_threshold'] # or not be in a high stakes round
            )
    )

class Node:
    def __init__(self, position, hand, river, betting_amount, player_money, round, k, action_history,owner, action, leaf=False, curr_level=0, raise_count=0, p1_hand_strength=None, p2_hand_strength=None, p1_hand_strength_rmse=None, p2_hand_strength_rmse=None, p2_dist=None, weight=1):
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
        self.raise_count = raise_count          # Number of Raises
        self.p1_hand_strength = p1_hand_strength
        self.p2_hand_strength = p2_hand_strength
        self.p1_hand_strength_rmse = p1_hand_strength_rmse
        self.p2_hand_strength_rmse = p2_hand_strength_rmse
        self.dist = p2_dist                     # Probability distribution of player 2's actions
        self.weight = weight                    # Weight of the node

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

        return None

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
        win_amount = self.pot
        lose_amount = -self.pot

        # params
        params = {}
        params['hand_info'] = {}
        params['hand_info']['p1_hand_strength'] = self.p1_hand_strength
        params['hand_info']['p2_hand_strength'] = self.p2_hand_strength
        params['hand_info']['p1_hand_strength_rmse'] = self.p1_hand_strength_rmse
        params['hand_info']['p2_hand_strength_rmse'] = self.p2_hand_strength_rmse
        params['num_round_raises'] = len(self.action_history) - self.round * 2 # in the safest gameplay, each player only CALLs, causing rounds to end in 2 moves each
        params['relative_betting_power'] = -inf if self.p1_money <= 0 else (self.p1_money - self.p2_money)/self.p1_money # (-inf, 1] where 1 => complete monopoly, 0 => equal wealth

        # Rules
        # If we fold, we will gain negative utility
        if self.owner == 1 and self.action == 'FOLD':
            return lose_amount

        # If they fold, we will gain positive utility
        if self.owner == 2 and self.action == 'FOLD':
            return win_amount

        # If nature controlled node, report positive utility
        if self.owner == 3:
            return win_amount # TODO: Revisit this

        # Complete victory: Our hand is stronger than anything the opponent's could be
        if determine_victory(params=params, risk_level='zero'):
            return win_amount

        # Narrow risk of defeat: There is a small chance that we might have a weaker hand
        if determine_victory(params=params, risk_level='low'):
            return win_amount

        # Moderate risk of defeat: There is a significant chance that either of us has the weaker hand
        if determine_victory(params=params, risk_level='med'):
            return win_amount

        # High risk of defeat: There is only a small chance that we might have a stronger hand
        if determine_victory(params=params, risk_level='high'):
            return win_amount

        # In all other cases, we expect to gain negative utility
        return lose_amount

    def calculate_bluff_probability(self):
        """
        calculate_bluff_probability returns the probability of the opponent bluffing throughout the game
        return: returns the value of opp_bluff_prob
        """
        opp_bluff_prob = 0
        if self.p1_money < self.p2_money:
            opp_bluff_prob += 0.1
        if self.p1_hand_strength < self.p2_hand_strength:
            opp_bluff_prob += 0.1
        return opp_bluff_prob

    def action_helper_player(self, next, money):
        """
        action_helper_player returns valid states for the player
        :next: next player
        :money: money of the player
        return: returns a list of states from valid actions
        """
        moves = [] # List of valid states
        missing_index = [1, 2]
        # Fold State
        moves.append((0, Node(
            position=self.position,
            hand=self.hand,
            river=self.river,
            betting_amount=self.betting_amount,
            player_money=[self.p1_money, self.p2_money, self.pot],
            round=self.round,
            k=self.k,
            action_history=[*self.action_history, (self.owner, 'FOLD', 0.0)],
            owner=self.owner,
            leaf=True,
            curr_level=self.curr_level+1,
            action='FOLD',
            p1_hand_strength=self.p1_hand_strength,
            p2_hand_strength=self.p2_hand_strength,
            p1_hand_strength_rmse=self.p1_hand_strength_rmse,
            p2_hand_strength_rmse=self.p2_hand_strength_rmse,
            p2_dist=self.dist
        )))

        # Call State
        if  money >= self.call_amount:
            if self.raise_count > 0:
                next = 3
                if self.position == 0 and self.owner == 1:
                    next_position = 1
                elif self.position == 0 and self.owner == 2:
                    next_position = 0
                elif self.position == 1 and self.owner == 1:
                    next_position = 1
                elif self.position == 1 and self.owner == 2:
                    next_position = 0
            else:
                next_position = self.position

            next_round = self.round + 1 if next == 3 else self.round
            is_k = self.k <= self.curr_level + 1 or next_round == 5  # Check if the depth limit is reached or the game is over 

            # Update the money of the player after calling
            d1 = self.p1_money - self.call_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.call_amount if self.owner == 2 else self.p2_money
            new_amounts = (0, 10) # Update the betting amounts

            moves.append((1, Node(
                position=next_position,
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
                raise_count=self.raise_count,
                p1_hand_strength=self.p1_hand_strength,
                p2_hand_strength=self.p2_hand_strength,
                p1_hand_strength_rmse=self.p1_hand_strength_rmse,
                p2_hand_strength_rmse=self.p2_hand_strength_rmse,
                p2_dist=self.dist,
            )))

            missing_index.remove(1)

        # Raise State
        if  money >= self.raise_amount and self.raise_count <= 4:
            # Update the money of the player after raising
            d1 = self.p1_money - self.raise_amount if self.owner == 1 else self.p1_money
            d2 = self.p2_money - self.raise_amount if self.owner == 2 else self.p2_money
            new_amounts = (10, 20) #updating the betting amounts
                   
            next = 2 if self.owner == 1 else 1
            next_round = self.round
            is_k = self.k <= self.curr_level + 1 or next_round == 5 

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
                raise_count=self.raise_count+1,
                p1_hand_strength=self.p1_hand_strength,
                p2_hand_strength=self.p2_hand_strength,
                p1_hand_strength_rmse=self.p1_hand_strength_rmse,
                p2_hand_strength_rmse=self.p2_hand_strength_rmse,
                p2_dist=self.dist
            )))
            missing_index.remove(2)
        
        if self.owner == 2:
            if len(missing_index) != 0:
                change_distibution = self.dist.copy()
                unavailable = change_distibution[missing_index].sum()
                change_distibution[missing_index] = 0
                change_distibution += unavailable*change_distibution / change_distibution.sum()
                self.dist = change_distibution
            for state in moves:
                state[1].dist = self.dist
                state[1].weight = self.dist[state[0]]

        return moves



    def action_helper_nature(self, next):
        """
        action_helper_nature returns valid states for nature
        :next: next player
        return: returns a list of states from valid actions
        """

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
        moves = []
        if num_cards == 3:
            valid_combinations = list(combinations(remaining_cards, num_cards))
            for branch in valid_combinations:
                p1_hand_strength, p2_hand_strength, p1_hand_strength_rmse, p2_hand_strength_rmse = calculate_hand_strength(self.hand, branch) # Note: hand will always be our (player 1's) cards

                moves.append((-1, Node(
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
                    p1_hand_strength=p1_hand_strength,
                    p2_hand_strength=p2_hand_strength,
                    p1_hand_strength_rmse=p1_hand_strength_rmse,
                    p2_hand_strength_rmse=p2_hand_strength_rmse,
                    p2_dist=self.dist
                )))

        else:
            for card in remaining_cards:
                p1_hand_strength, p2_hand_strength, p1_hand_strength_rmse, p2_hand_strength_rmse = calculate_hand_strength(self.hand, self.river + [card]) # Note: hand will always be our (player 1's) cards

                moves.append((-1, Node(
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
                    p1_hand_strength=p1_hand_strength,
                    p2_hand_strength=p2_hand_strength,
                    p1_hand_strength_rmse=p1_hand_strength_rmse,
                    p2_hand_strength_rmse=p2_hand_strength_rmse,
                    p2_dist=self.dist
                )))

        return moves
