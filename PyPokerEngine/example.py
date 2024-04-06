from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.console_player import ConsolePlayer
# from PyPokerEngine.examples.players.fish_player import FishPlayer
#TODO:config the config as our wish
config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=10)



config.register_player(name="f1", algorithm=FishPlayer())
config.register_player(name="FT2", algorithm=ConsolePlayer())


game_result = start_poker(config, verbose=0)
