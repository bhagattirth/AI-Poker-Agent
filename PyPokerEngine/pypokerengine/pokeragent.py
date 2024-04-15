from pypokerengine.players import BasePokerPlayer
from pypokerengine.pokerAgent.tree import Tree
import time

class PokerAgent(BasePokerPlayer):

  def declare_action(self, valid_actions, hole_card, round_state):
    start = time.time()
    position = 0 if round_state["next_player"] == round_state["small_blind_pos"] else 1
    street = round_state["street"]
    if street == "preflop":
      round = 1
    elif street == "flop":
      round = 2
    elif street == "turn":
      round = 3
    elif street == "river":
      round = 4
    
    community_card = round_state["community_card"]
    p1_money = round_state["seats"][round_state["next_player"]]["stack"]
    p2_money = round_state["seats"][1 if round_state["next_player"] == 0 else 0]["stack"]
    pot = round_state["pot"]["main"]["amount"]
    last_move = round_state["action_histories"][street][-1]
    call_amount = last_move["paid"] if "paid" in last_move else last_move["add_amount"]
    raise_amount = 10 + call_amount
    k = 3

    tree = Tree(position, hole_card, community_card, call_amount, raise_amount, p1_money, p2_money, pot, round, k)
    action = tree.pick_Action()
    move = valid_actions[action]

    if action == 2:
      return move["action"], raise_amount
    
    end = time.time()
    print("Time taken: ", end - start)
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