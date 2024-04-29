from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.honest_player import HonestPlayer
from examples.players.console_player import ConsolePlayer
from pypokerengine.pokeragent import PokerAgent
# from PyPokerEngine.examples.players.fish_player import FishPlayer
#TODO:config the config as our wish
config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)



config.register_player(name="fish", algorithm=FishPlayer())
# config.register_player(name="cli", algorithm=ConsolePlayer()) # uncomment for to enter into interactive gameplay
config.register_player(name="PokerMan", algorithm=PokerAgent())


game_result = start_poker(config, verbose=1)
