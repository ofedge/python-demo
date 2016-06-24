#! /usr/bin/env python3
import time
import threading


def timer_func(msg1):
    print("I'm test_func,", msg1)


def timer_start():
    while True:
        t = threading.Timer(0, timer_func, ("parameter1",))
        t.start()
        time.sleep(24 * 60 * 60)


if __name__ == '__main__':
    timer_start()
