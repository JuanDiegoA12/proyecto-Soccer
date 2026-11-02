import socket
import time

SERVER_HOST = "localhost"
SERVER_PORT = 6000
BUFFER_SIZE = 4096


class BasePlayer:
    def __init__(self, team_name, number, role):
        self.team_name = team_name
        self.number = number
        self.role = role

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 0))

    def send_to(self, msg, port):
        self.sock.sendto(msg.encode(), (SERVER_HOST, port))
        print(f"[{self.role}-{self.number}] -> {msg} (puerto={port})")

    def send(self, msg):
        self.send_to(msg, SERVER_PORT)

    def receive(self, timeout=None):
        if timeout:
            self.sock.settimeout(timeout)
        else:
            self.sock.settimeout(None)
        try:
            data, _ = self.sock.recvfrom(BUFFER_SIZE)
            msg = data.decode()
            return msg
        except socket.timeout:
            return ""
        except Exception as e:
            print(e)
            return ""

    def start_position(self):
        positions_map = {
            1: (-52.5, 0),
            2: (-35, -20),
            3: (-35, -7),
            4: (-35, 7),
            5: (-35, 20),
            6: (-10, 15),
            7: (0, 15),
            8: (10, 15),
            9: (-10, 25),
            10: (0, 25),
            11: (10, 25),
        }
        return positions_map.get(self.number, (0, 0))

    def init_connection(self):
        if self.role == "goalkeeper":
            init_msg = f"(init {self.team_name} (goalie))"
        else:
            init_msg = f"(init {self.team_name})"

        self.send(init_msg)

        while True:
            msg = self.receive()
            if msg and self.is_pre_kickoff_or_play(msg):
                print(f"[{self.role}-{self.number}] <- INIT OK")

                x, y = self.start_position()
                self.send(f"(move {x} {y})")
                print(f"[{self.role}-{self.number}] -> MOVE a ({x},{y})")
                break

    def play(self):
        self.send("(dash 50)")

    def is_pre_kickoff_or_play(self, msg: str) -> bool:
        keywords = ["before_kick_off", "(init", "play_on"]
        return any(keyword in msg for keyword in keywords)

    def action_loop(self):
        while True:
            msg = self.receive()
            if msg and self.is_pre_kickoff_or_play(msg):
                x, y = self.start_position()
                self.send(f"(move {x} {y})")
            else:
                self.play()
            time.sleep(0.1)

    def start(self):
        self.init_connection()
        self.action_loop()
