#!/usr/bin/env python

"""baboon_problem.py: Solve the baboon semaphore problem.
1. Once a baboon has begun to cross the canyon it is guaranteed to get across.
2. There are never more than 5 baboons on the rope
3. A continuing stream of baboons in one direction should not lock out the other 
direction from crossing eventually."""

__author__ = "Justin Overstreet"
__copyright__ = "oversj96.github.io"

import threading
from random import *
import time

directions = ['left', 'right']
# baboons is a Semaphore object with acquire and release as built-in
# functions. These functions act as wait and signal respectively.
baboons = threading.Semaphore(0)
left_count = 0
right_count = 0
rope = threading.Semaphore(1)
direction = 'left'


def crossing():
    global right_count
    global left_count
    global direction
    while True:
        baboons.acquire() 
        print("A baboon is attempting to cross")
        rope.acquire()
        print(f"A baboon has the rope and is going {direction}.")
        if direction is 'left' and left_count > 0:
            left_count -= 1
            direction = 'right'
        elif direction is 'right' and right_count > 0:
            right_count -= 1
            direction = 'left'
        print(f"A baboon has crossed from the {direction}")
        rope.release() # release acts like signal
        print("A baboon has released the rope.")

def baboon(travel_direction):
    global left_count
    global right_count
    baboons.release()
    print(f"A baboon has arrived wanting to go {travel_direction}.")
    if travel_direction is "left":          
        left_count += 1
    else:
        right_count += 1


def generate_baboons():
    global directions
    while True:
        if (right_count + left_count) > 100:
            print("The baboon line is full!")
            print(f"The right side has {right_count} ape(s).")
            print(f"The left side has {left_count} ape(s).")
            time.sleep(1)
        else:
            baboon(sample(directions, 1)[0])

if __name__ == "__main__":
    t = threading.Thread(target = crossing)
    t.start()
    t2 = threading.Thread(target = generate_baboons)
    t2.start()