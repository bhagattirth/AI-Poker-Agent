from pypokerengine.players import BasePokerPlayer
from pypokerengine.pokerAgent.tree import Tree
from time import time

class PokerAgent(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    print("start")
    start = time()
    position = 0 if round_state["next_player"] == round_state["small_blind_pos"] else 1 # 0 = SB, 1 = BB
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
    p1_money = round_state["seats"][round_state["next_player"]]["stack"]                  # PokerAgent Money
    p2_money = round_state["seats"][1 if round_state["next_player"] == 0 else 0]["stack"] # Opponent Money
    pot = round_state["pot"]["main"]["amount"]                                            # Pot Amount
    call_amount = valid_actions[1]["amount"]                                              # Call Amount
    raise_amount = 10 + call_amount                                                       # Raise Amount                       
    k = 5                                                                                 # Depth Limit


    tree = Tree(position, hole_card, community_card, call_amount, raise_amount, p1_money, p2_money, pot, round, k)
    action = tree.pick_Action() # Returns "Optimal" move: 0 = Fold, 1 = Call, 2 = Raise
    move = valid_actions[action]


    end = time()
    print("Time taken: ", end - start)

    if action == 2: # Raise
      return move["action"], raise_amount
    
    return move["action"], move["amount"]

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

# def setup_ai():
#   return RandomPlayer()