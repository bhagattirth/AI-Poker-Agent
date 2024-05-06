from pypokerengine.players import BasePokerPlayer
from .pokerAgent.tree import Tree
from .pokerAgent.node import calculate_hand_strength
from time import time
from statistics import variance
import numpy as np

stats = []

starting_stack = 0
raising_odds = 1
call_odds = 1
raise_odds = 1
sum_val = 3
stack_history = []


class PokerAgent(BasePokerPlayer):
  def declare_action(self, valid_actions, hole_card, round_state):
    start = time()
    position = 0 if round_state["next_player"] == round_state["small_blind_pos"] else 1 # 0 = Small Blind, 1 = Big Blind
    street = round_state["street"]  # Name of the round
    if street == "preflop":
      round = 1
    elif street == "flop":
      round = 2
    elif street == "turn":
      round = 3
    elif street == "river":
      round = 4

    community_card = round_state["community_card"]                                        # River Cards
    p1_info = round_state["seats"][round_state["next_player"]]
    p2_info = round_state["seats"][1 if round_state["next_player"] == 0 else 0]
    p1_money = p1_info["stack"]                                                           # PokerAgent Money
    p2_money = p2_info["stack"]                                                           # Opponent Money
    pot = round_state["pot"]["main"]["amount"]                                            # Pot Amount
    call_amount = 0 if valid_actions[1]["amount"] == 0 else 10                            # Call Amount
    raise_amount = 10 if call_amount == 0 else 20                                         # Raise Amount
    raise_count = 0

    for item in round_state['action_histories'][street]:
      if item['action'] == 'RAISE':
        raise_count += 1

    k = 3                                                                                 # Depth Limit
    action_history = [(
          1 if item['uuid'] == p1_info['uuid'] else 2,
          item['action'],
          item['paid'] if 'paid' in item else item['add_amount']
      ) for (k,v) in round_state['action_histories'].items() for item in v]               # Action History

    global raising_odds
    global call_odds
    global raise_odds
    global sum_val

    last_actions = action_history[-1]
    if last_actions[1] == 'RAISE' and last_actions[0] == 2:
      raise_odds += 1
      sum_val += 1
    elif last_actions[1] == 'CALL' and last_actions[0] == 2:
      call_odds += 1
      sum_val += 1
    elif last_actions[1] == 'RAISE' and last_actions[0] == 1:
      raising_odds += 1
      sum_val += 1

    p2_dist = np.array([raising_odds/(sum_val), call_odds/(sum_val), raise_odds/(sum_val)])

    # p2_dist = np.array([raising_odds/(raising_odds + call_odds + raise_odds + 3), 
    #            call_odds/(raising_odds + call_odds + raise_odds + 3), 
    #            raise_odds/(raising_odds + call_odds + raise_odds + 3)])
    

    tree = Tree(
      position=position,
      hand=hole_card,
      river=community_card,
      call_amount=call_amount,
      raise_amount=raise_amount,
      p1Money=p1_money,
      p2Money=p2_money,
      pot=pot,
      round=round,
      k=k,
      action_history=action_history,
      aggression=0,
      raise_count=raise_count,
      p2_dist=p2_dist
    )
    action = tree.pick_Action() # Returns "Optimal" move: 0 = Fold, 1 = Call, 2 = Raise
    move = valid_actions[action]


    end = time()
    print("Time taken: ", end - start)

    ## REMOVE THE BELOW BLOCK
    stats[-1]['time_taken'].append(end - start)
    stats[-1]['decisions'].append(move["action"])

    if action == 2: # Raise
      return move["action"], move["amount"]["min"]

    return move["action"], move["amount"]

  def receive_game_start_message(self, game_info):
    global stack_history
    stack_history.append(game_info['rule']['initial_stack'])

  def receive_round_start_message(self, round_count, hole_card, seats):
    stats.append({
      'time_taken': [],
      'decisions': [],
      'outcome': None,
      'hand': hole_card,
    })

    print(f'\n\n-+-+-[Round {round_count}]-+-+-\n')
    print("Cards in hand: ", hole_card)

  def receive_street_start_message(self, street, round_state):
    print(f'\n--[{street}]--')

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    stats[-1]['outcome'] = winners[0]['name'] == 'PokerMan'
    stats[-1]['river'] = round_state['community_card']
    stack_history.append([seat['stack'] for seat in round_state['seats'] if seat['name'] == 'PokerMan'][0])

    p1_hand_str, p2_hand_str, _, p2_hand_str_rmse = calculate_hand_strength(stats[-1]['hand'], stats[-1]['river'])
    stats[-1]['hand_strength'] = p1_hand_str
    stats[-1]['opp_hand_strength'] = p2_hand_str
    stats[-1]['opp_hand_strength_rmse'] = p2_hand_str_rmse

    action_history = [(
          1 if item['uuid'] == round_state["seats"][round_state["next_player"]]['uuid'] else 2,
          item['action'],
          item['paid'] if 'paid' in item else item['add_amount'] if 'add_amount' in item else 0.0
      ) for (k,v) in round_state['action_histories'].items() for item in v]

    print(f"\nHand strength this round\n  Ours: {stats[-1]['hand_strength']}\nTheirs: {stats[-1]['opp_hand_strength']} (rmse: {stats[-1]['opp_hand_strength_rmse']})")
    print(f"\nPlay this round (player, move, amount added) => {action_history}")

    outcomes = [stat['outcome'] for stat in stats]
    winnings = [stack_history[idx + 1] - stack_history[idx] for idx, outcome in enumerate(outcomes) if outcome]
    losses = [stack_history[idx + 1] - stack_history[idx] for idx, outcome in enumerate(outcomes) if not outcome]

    won_rounds_hand_strengths = [stats[idx]['hand_strength'] for idx, outcome in enumerate(outcomes) if outcome]
    won_rounds_opp_hand_strengths = [stats[idx]['opp_hand_strength'] for idx, outcome in enumerate(outcomes) if outcome]
    won_rounds_opp_hand_strengths_rmse = [stats[idx]['opp_hand_strength_rmse'] for idx, outcome in enumerate(outcomes) if outcome]
    lost_rounds_hand_strengths = [stats[idx]['hand_strength'] for idx, outcome in enumerate(outcomes) if not outcome]
    lost_rounds_opp_hand_strengths = [stats[idx]['opp_hand_strength'] for idx, outcome in enumerate(outcomes) if not outcome]
    lost_rounds_opp_hand_strengths_rmse = [stats[idx]['opp_hand_strength_rmse'] for idx, outcome in enumerate(outcomes) if not outcome]

    print(f"\nWe've earned ${stack_history[-1] - stack_history[0]} so far!")
    print(f"Average Winnings: ${(sum(winnings)/len(winnings)) if len(winnings) else 0.0} in {len(winnings)} rounds (higher is better)")
    print(f"Average Losses: ${(sum(losses)/len(losses)) if len(losses) else 0.0} in {len(losses)} rounds (lower is better)")

    if len(won_rounds_hand_strengths) > 1: # variance fn needs at least 2 data points
      average_won_hand_strength = sum(won_rounds_hand_strengths)/len(won_rounds_hand_strengths)
      won_hand_strength_var = variance(won_rounds_hand_strengths, average_won_hand_strength)

      average_won_opp_hand_strength = sum(won_rounds_opp_hand_strengths)/len(won_rounds_hand_strengths)
      won_opp_hand_strength_var = variance(won_rounds_opp_hand_strengths, average_won_opp_hand_strength)
      
      average_won_opp_hand_strength_rmse = sum(won_rounds_opp_hand_strengths_rmse)/len(won_rounds_hand_strengths)
      won_opp_hand_strength_rmse_var = variance(won_rounds_opp_hand_strengths_rmse, average_won_opp_hand_strength_rmse)
      print("\nHand Strength Stats [Won] (average)")
      print(f"ours: {average_won_hand_strength} (Var: {won_hand_strength_var}, higher is better)")
      print(f" opp: {average_won_opp_hand_strength} (Var: {won_opp_hand_strength_var}) [rmse: {average_won_opp_hand_strength_rmse} (Var: {won_opp_hand_strength_rmse_var})]")

    if len(lost_rounds_hand_strengths) > 1: # variance fn needs at least 2 data points
      average_lost_hand_strength = sum(lost_rounds_hand_strengths)/len(lost_rounds_hand_strengths)
      lost_hand_strength_var = variance(lost_rounds_hand_strengths, average_lost_hand_strength)

      average_opp_hand_strength = sum(lost_rounds_opp_hand_strengths)/len(lost_rounds_hand_strengths)
      opp_hand_strength_var = variance(lost_rounds_opp_hand_strengths, average_opp_hand_strength)

      average_lost_opp_hand_strength_rmse = sum(lost_rounds_opp_hand_strengths_rmse)/len(lost_rounds_hand_strengths)
      lost_opp_hand_strength_rmse_var = variance(lost_rounds_opp_hand_strengths_rmse, average_lost_opp_hand_strength_rmse)

      print("\nHand Strength Stats [Lost] (average)")
      print(f"ours: {average_lost_hand_strength} (Var: {lost_hand_strength_var}, lower is better)")
      print(f" opp: {average_opp_hand_strength} (Var: {opp_hand_strength_var}) [rmse: {average_lost_opp_hand_strength_rmse} (Var: {lost_opp_hand_strength_rmse_var})]")
