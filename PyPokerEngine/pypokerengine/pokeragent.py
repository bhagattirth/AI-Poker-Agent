from pypokerengine.players import BasePokerPlayer
from pypokerengine.pokerAgent.tree import Tree
from time import time

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
    raise_amount = 10 + call_amount                                                       # Raise Amount                       
    k = 3                                                                                 # Depth Limit
    action_history = [(
          1 if item['uuid'] == p1_info['uuid'] else 2, 
          item['action'], 
          item['paid'] if 'paid' in item else item['add_amount']
      ) for (k,v) in round_state['action_histories'].items() for item in v]               # Action History
    print(f"Play so far (player, move, amount added) => {action_history}")


    tree = Tree(position, hole_card, community_card, call_amount, raise_amount, p1_money, p2_money, pot, round, k, action_history)
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
      'winnings': []
    })
    print('\n--[Round]--\n')
    print("Cards in hand: ", hole_card)

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    stats[-1]['winnings'].append(round_state['pot']['main']['amount'])
    print("Stats: ", stats[-1])
    print(round_state['action_histories'])

# def setup_ai():
#   return RandomPlayer()