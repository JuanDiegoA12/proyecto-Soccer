from qlearner import QLearner
import sys


class Attacker(QLearner):
    pass


if __name__ == "__main__":
    number = int(sys.argv[1])
    role = sys.argv[2]
    player = Attacker(team_name="MYTEAMUD", number=number, role=role)
    player.start()
