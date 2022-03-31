#!/usr/bin/env python

"""Client"""

import argparse
import random
import socket
import time

FORMAT: str = "UTF-8"
MSG_B: int = 4096


def alice(act):
    """"""

    return f"I think {act + 'ing'} sounds great!"


def bob(act, act_b=None):
    if act_b is None:
        return f"Not sure about {act + 'ing'}. Don't I get a choice?"
    return f"Sure, both {act + 'ing'} and {act_b + 'ing'} seems ok to me"


def chuck(act):
    act = act + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]
    if act in bad_things:
        return f"YESS! Time for {act}"
    elif act in good_things:
        return f"What? {act} sucks. Not doing that."
    return "I don't care!"


def dora(act):
    alternatives = ["coding", "shooting", "sleeping"]
    act_b = random.choice(alternatives)
    res = f"Yea, {act}ing is an option. Or we could do some {act_b}."
    return res


def bot_func(num, act):

    match num:
        case 1:
            return alice(act)
        case 2:
            return bob(act)
        case 3:
            return chuck(act)
        case 4:
            return dora(act)


IP_TEXT: str = "Ip address of client"
PORT_TXT: str = "Port of server you are trying to connect to"
BOT_TXT: str = "The client's name (your username)"

parser = argparse.ArgumentParser()

parser.add_argument("ip", metavar="IP", help=IP_TEXT, type=str)
parser.add_argument("port", metavar="Port", help=PORT_TXT, type=int)
parser.add_argument("bot", metavar="Bot", help=BOT_TXT, type=str)

args = parser.parse_args()

bot: str = args.bot
bot_num: int = random.randint(1, 4)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((args.ip, args.port))

s.send(bot.encode(FORMAT))

while True:
    msg_r = s.recv(MSG_B).decode(FORMAT)

    if msg_r == f"{bot} ACTIVATE":
        break

    print(2)
    print(msg_r)


while True:

    try:
        msg_r = s.recv(MSG_B).decode(FORMAT)
    except OSError:
        print("Server disconnected")
        break

    print(msg_r)

    if msg_r == "Bye!":
        s.send("Bye!".encode(FORMAT))
        break

    action_2: str = msg_r[26:-1]

    msg_s: str = bot_func(bot_num, action_2)

    time.sleep(1)

    s.send(f"{bot}: {msg_s}".encode(FORMAT))

    print(f"\nMe: {msg_s}")

s.shutdown(socket.SHUT_RDWR)
s.close()
print("\nThe client is now closed")
