from pypokerengine.players import BasePokerPlayer
from .pokerAgent.tree import Tree
from time import time
from .pokerAgent.abstraction import Abstraction

stats = []

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
    p1_money = p1_info["stack"]                                      # PokerAgent Money
    p2_money = p2_info["stack"]                                      # Opponent Money
    pot = round_state["pot"]["main"]["amount"]                                            # Pot Amount
    call_amount = valid_actions[1]["amount"]                                              # Call Amount
    raise_amount = valid_actions[2]["amount"]["min"]                                      # Raise Amount
    k = 3                                                                                 # Depth Limit
    action_history = [(
          1 if item['uuid'] == p1_info['uuid'] else 2,
          item['action'],
          item['paid'] if 'paid' in item else item['add_amount']
      ) for (k,v) in round_state['action_histories'].items() for item in v]               # Action History
    
    # TPT_zip=Abstraction.tpt_table()
    TPT_zip=[]
    print("Table fetched, Time taken: ", time() - start)

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
      TPT=TPT_zip
    )
    action = tree.pick_Action() # Returns "Optimal" move: 0 = Fold, 1 = Call, 2 = Raise
    move = valid_actions[action]


    end = time()
    print("Time taken: ", end - start)

    ## REMOVE THE BELOW BLOCK
    stats[-1]['time_taken'].append(end - start)
    stats[-1]['decisions'].append(move["action"])

    if action == 2: # Raise
      return move["action"], raise_amount

    return move["action"], move["amount"]

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    stats.append({
      'time_taken': [],
      'decisions': [],
      'outcome': None
    })
    print('\n\n-+-+-[Round]-+-+-\n')
    print("Cards in hand: ", hole_card)

  def receive_street_start_message(self, street, round_state):
    print(f'\n--[{street}]--')

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    stats[-1]['outcome'] = winners[0]['name'] == 'PokerMan'

    action_history = [(
          1 if item['uuid'] == round_state["seats"][round_state["next_player"]]['uuid'] else 2,
          item['action'],
          item['paid'] if 'paid' in item else item['add_amount'] if 'add_amount' in item else 0.0
      ) for (k,v) in round_state['action_histories'].items() for item in v]
    outcomes = [stat['outcome'] for stat in stats]
    print(f"\n\nPlay this round (player, move, amount added) => {action_history}")
    print(f"We've earned ${round_state['seats'][1 if round_state['next_player'] == 0 else 1]['stack'] - 1000} so far!\nWon {sum(outcomes)}/{len(outcomes)} rounds (Winning rate: {100*sum(outcomes)/len(outcomes)}%)")
