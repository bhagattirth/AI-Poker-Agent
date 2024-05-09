from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.honest_player import HonestPlayer
from examples.players.console_player import ConsolePlayer
from examples.players.random_player import RandomPlayer
from pokeragent import PokerAgent
# from PyPokerEngine.examples.players.fish_player import FishPlayer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--rounds', type=int, default=50)
parser.add_argument('--stack', type=int, default=1000)
parser.add_argument('--interactive', '-i', action='store_true')
parser.add_argument('--data', '-d', action='store_true')
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

#TODO:config the config as our wish
config = setup_config(max_round=args.rounds, initial_stack=args.stack, small_blind_amount=10)

pokerman = PokerAgent(verbose=2 if args.verbose else 1)
clone = PokerAgent(verbose=0)

if args.interactive:
    config.register_player(name="cli", algorithm=ConsolePlayer())
else:
    # config.register_player(name="Clone", algorithm=clone)
    config.register_player(name="Honest", algorithm=HonestPlayer())
    # config.register_player(name="Fish", algorithm=FishPlayer())
    # config.register_player(name="Random", algorithm=RandomPlayer())

config.register_player(name="PokerMan", algorithm=pokerman)

game_result = start_poker(config, verbose=1)

if args.data:
    pokerman.report_stats()
    pokerman.save_stats()
