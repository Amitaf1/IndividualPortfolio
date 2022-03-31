"""Server"""

import argparse
import random
import socket
import threading
import time

FORMAT: str = "UTF-8"
MSG_B: int = 4096
clients: list = []
active_conv: bool = False


def main(con_par: socket, addr_par):

    """Main function that each thread will run"""

    c_id: str = con_par.recv(MSG_B).decode()

    print(f"Connection from: {addr_par}")

    global active_conv, clients
    clients.append(c_id)

    while True:
        if not active_conv:
            active_conv = True
            con_par.send(f"{c_id} ACTIVATE".encode(FORMAT))
            break
        else:
            continue

    while True:

        action: str = random.choice(
            ["work", "play", "eat", "cry", "sleep", "fight", "sing", "yell"])

        end_var: str = input(
            "Do you want to continue the dialogue? (blank -> continue): ")

        try:
            if end_var != "":
                con_par.send("Bye!".encode(FORMAT))
                print(con_par.recv(MSG_B).decode(FORMAT))
                break

            msg_s = (f"Do you guys want to {action}?")

            time.sleep(1)

            con_par.send(f"Host: {msg_s}".encode(FORMAT))
            print(f"\nMe: {msg_s}")

            msg_r = con_par.recv(MSG_B).decode(FORMAT)

            print(f"\n{msg_r}")

        except ConnectionResetError:
            print("Client disconnected")
            break

    clients.remove(c_id)
    if clients:
        first_client = clients[0]
        print(first_client)
        con_par.send(f"{first_client} ACTIVATE".encode(FORMAT))
    con_par.shutdown(socket.SHUT_RDWR)
    con_par.close()
    active_conv = False


parser = argparse.ArgumentParser(description="Server")

parser.add_argument("port", metavar="Port", help="Port of server", type=int)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", parser.parse_args().port))

sock.listen()

while True:

    try:
        con, addr = sock.accept()
    except OSError:
        print("There are no more clients queued")
        break

    thread = threading.Thread(target=main, args=(con, addr))
    thread.start()
    print(clients)
