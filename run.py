from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.honest_player import HonestPlayer
from examples.players.console_player import ConsolePlayer
from examples.players.random_player import RandomPlayer
from examples.players.fold_man import FoldMan
from Group6Player import Group6Player
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--matches', type=int, default=1)
parser.add_argument('--rounds', type=int, default=50)
parser.add_argument('--stack', type=int, default=1000)
parser.add_argument('--data', '-d', action='store_true')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--opp', default='honest')
args = parser.parse_args()

for match in range(args.matches):
    config = setup_config(max_round=args.rounds, initial_stack=args.stack, small_blind_amount=10)
    if args.opp == 'cli':
        config.register_player(name="cli", algorithm=ConsolePlayer())
    elif args.opp == 'clone':
        config.register_player(name="Clone", algorithm=Group6Player(verbose=0))
    elif args.opp == 'fish':
        config.register_player(name="Fish", algorithm=FishPlayer())
    elif args.opp == 'random':
        config.register_player(name="Random", algorithm=RandomPlayer())
    elif args.opp == 'fold':
        config.register_player(name="Fold", algorithm=FoldMan())
    else:
        config.register_player(name="Honest", algorithm=HonestPlayer())

    pokerman = Group6Player(verbose=2 if args.verbose else 1)
    config.register_player(name="PokerMan", algorithm=pokerman)

    game_result = start_poker(config, verbose=1)

    if args.data:
        pokerman.report_stats(f"{args.opp}_results.csv")
        # pokerman.save_stats(f"{args.opp}_stats_{match}.pkl")
