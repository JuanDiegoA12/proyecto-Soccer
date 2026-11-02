import re
import sys
import time

import numpy as np
import pandas as pd

from base_player import BasePlayer


ANGLE_BINS = ["izq", "centro", "der"]
DIST_BINS = ["cerca", "media", "lejos"]
NO_BALL_STATE = "no_veo_balon"

ACTIONS = ["turn_left", "turn_right", "dash"]


def build_state_list():
    states = [f"{a}_{d}" for a in ANGLE_BINS for d in DIST_BINS]
    states.append(NO_BALL_STATE)
    return states


STATES = build_state_list()
STATE_INDEX = {s: i for i, s in enumerate(STATES)}


ALPHA = 0.2
GAMMA = 0.9
EPSILON = 0.2

Q_TABLE_FILE = "q_table.csv"


class QLearner(BasePlayer):
    def __init__(self, team_name, number, role):
        super().__init__(team_name, number, role)

        self.q = np.zeros((len(STATES), len(ACTIONS)))

        self.prev_state = None
        self.prev_action = None
        self.prev_ball = None

        self.rng = np.random.default_rng()

        self.q_table_file = f"q_table_{self.role}_{self.number}.csv"

    def parse_ball(self, msg):
        match = re.search(r"\(\((?:b|ball|B)\)\s+([-\d.]+)\s+([-\d.]+)", msg)
        if not match:
            return None
        distancia = float(match.group(1))
        angulo = float(match.group(2))
        return distancia, angulo

    def to_state(self, ball):
        if ball is None:
            return NO_BALL_STATE

        distancia, angulo = ball

        if angulo < -10:
            a = "izq"
        elif angulo > 10:
            a = "der"
        else:
            a = "centro"

        if distancia < 10:
            d = "cerca"
        elif distancia < 25:
            d = "media"
        else:
            d = "lejos"

        return f"{a}_{d}"

    def reward(self, ball, action_idx, prev_ball):
        if ball is None:
            return -1.0

        distancia, angulo = ball
        action = ACTIONS[action_idx]
        r = 0.0

        if prev_ball is not None:
            prev_dist, prev_ang = prev_ball
            if distancia < prev_dist:
                r += 1.0
            else:
                r -= 1.0

            if action == "dash" and abs(prev_ang) <= 10:
                r += 1.5
            elif action == "turn_left" and prev_ang < -10:
                r += 0.5
            elif action == "turn_right" and prev_ang > 10:
                r += 0.5

        return r

    def choose_action(self, state_idx):
        if self.rng.random() < EPSILON:
            return self.rng.integers(len(ACTIONS))
        return int(np.argmax(self.q[state_idx]))

    def update_q(self, s, a, r, s_next):
        mejor_futuro = np.max(self.q[s_next])
        td_error = r + GAMMA * mejor_futuro - self.q[s][a]
        self.q[s][a] += ALPHA * td_error

    def do_action(self, action_idx):
        action = ACTIONS[action_idx]
        if action == "turn_left":
            self.send("(turn -20)")
        elif action == "turn_right":
            self.send("(turn 20)")
        elif action == "dash":
            self.send("(dash 60)")

    def play(self):
        msg = getattr(self, "last_msg", "")

        ball = self.parse_ball(msg)

        if ball is None:
            self.send("(turn 60)")
            self.prev_state = None
            self.prev_action = None
            self.prev_ball = None
            return

        state = self.to_state(ball)
        state_idx = STATE_INDEX[state]

        if self.prev_state is not None:
            r = self.reward(ball, self.prev_action, self.prev_ball)
            self.update_q(self.prev_state, self.prev_action, r, state_idx)

        action_idx = self.choose_action(state_idx)
        self.do_action(action_idx)

        self.prev_state = state_idx
        self.prev_action = action_idx
        self.prev_ball = ball

    def action_loop(self):
        steps = 0
        self.send("(change_view wide normal)")
        while True:
            msg = self.receive(timeout=2)

            if msg and self.is_pre_kickoff_or_play(msg) and "(see" not in msg:
                x, y = self.start_position()
                self.send(f"(move {x} {y})")
                continue

            if "(see" in msg:
                self.last_msg = msg
                self.play()
                steps += 1

                if steps % 100 == 0:
                    self.save_q_table()

            time.sleep(0.05)

    def save_q_table(self):
        df = pd.DataFrame(self.q, index=STATES, columns=ACTIONS)
        df.to_csv(self.q_table_file)
        print(f"[{self.role}-{self.number}] Q-table guardada en {self.q_table_file}")


if __name__ == "__main__":
    number = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    role = sys.argv[2] if len(sys.argv) > 2 else "attacker"
    player = QLearner(team_name="MYTEAMUD", number=number, role=role)
    player.start()
