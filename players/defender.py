from base_player import BasePlayer
import sys
import random


class Defender(BasePlayer):
    def play(self):
        """Defensas se mueven y giran aleatoriamente"""
        ACTIONS = ["turn_left", "turn_right", "dash", "kick"]
        action = random.choice(ACTIONS)
        if action == "turn_left":
            self.send("(turn -45)")
        elif action == "turn_right":
            self.send("(turn 45)")
        elif action == "dash":
            self.send("(dash 60)")
        elif action == "kick":
            self.send("(kick 80 0)")


if __name__ == "__main__":
    number = int(sys.argv[1])
    role = sys.argv[2]
    player = Defender(team_name="MYTEAMUD", number=number, role=role)
    player.start()
