import subprocess
import sys
import time

ROLES = {"goalkeeper": 1, "defender": 4, "attacker": 6}


def launch_player(role, number):
    path = f"players/{role}.py"
    proc = subprocess.Popen(
        [sys.executable, path, str(number), role],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    print(f"  -> {role.capitalize()} #{number} pid={proc.pid}")
    return {"proc": proc, "number": number, "role": role}


def monitor_process(player):
    proc = player["proc"]
    while True:
        line = proc.stdout.readline()
        if line:
            print(f"[{player['role']}-{player['number']}] {line.strip()}")
        err = proc.stderr.readline()
        if err:
            print(f"[{player['role']}-{player['number']}] ERR: {err.strip()}")
        if proc.poll() is not None:
            break


def main():
    processes = []

    player_number = 1
    processes.append(launch_player("goalkeeper", player_number))
    player_number += 1

    for _ in range(ROLES["defender"]):
        processes.append(launch_player("defender", player_number))
        player_number += 1

    for _ in range(ROLES["attacker"]):
        processes.append(launch_player("attacker", player_number))
        player_number += 1

    print("\nTodos los jugadores lanzados. Monitoreando...\n")

    import threading
    for player in processes:
        threading.Thread(
            target=monitor_process,
            args=(player,),
            daemon=True
        ).start()

    try:
        while True:
            time.sleep(1)
            for i, player in enumerate(processes[:]):
                proc = player["proc"]
                if proc.poll() is not None:
                    print(
                        f"❌ [{player['role']}-{player['number']}] murió...."
                    )
                    print("Reiniciando..")
                    new_player = launch_player(
                        player["role"],
                        player["number"]
                    )
                    processes[i] = new_player
                    threading.Thread(
                        target=monitor_process,
                        args=(new_player,),
                        daemon=True
                    ).start()
    except KeyboardInterrupt:
        print("\nCerrando todos los jugadores...")
        for player in processes:
            player["proc"].terminate()
        print("Hecho.")


if __name__ == "__main__":
    main()
