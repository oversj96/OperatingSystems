#!/usr/bin/env python

"""tribe_of_savages.py: A tribe eats dinners from a pot that holds M shares.
When a savage wants to eat he helps himself, if the pot is empty he wakes the cook
the savages wait until the cook completely fills the pot. The cook refills only when
the pot is empty. There is only one cook and an arbitrary amount of savages. 
Solve using semaphores."""

__author__ = "Justin Overstreet"
__copyright__ = "oversj96.github.io"

import threading
from multiprocessing import Process
from random import *
import time

cook = threading.Semaphore(1)
pot_access = threading.Semaphore(1)
shares = 20 # can be any value


def fill_pot():
    global shares
    while True:
        print("The cook goes to sleep")
        cook.acquire()
        print("The cook is awake")
        pot_access.acquire()
        print("The cook has taken the pot")
        shares = 20
        pot_access.release()
        print("The cook has refilled the pot")


def savage():
    global shares
    print("A savage has come to eat!")
    if shares == 0:
        print("The pot is empty and a savage has woken the cook")
        cook.release()
    print("A savage wants to draw from the pot!")
    pot_access.acquire()
    print("A savage draws from the pot")
    shares -= 1
    pot_access.release()
    print("A savage has eaten and left")


def generate_savages():
    global shares
    while True:
        for i in range(1, randint(2, 30)):
            savage()
        print(f"There is {shares} share(s) left after {i} savage(s) ate.")
        time.sleep(randint(0, 5))


if __name__ == "__main__":
    p = threading.Thread(target = fill_pot)
    p2 = threading.Thread(target = generate_savages)
    p.start()
    p2.start()