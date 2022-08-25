#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import sys
import os

BLPATH = "/sys/class/leds/smc::kbd_backlight"
BLVALFILE = "brightness"
BLMAXFILE = "max_brightness"

def help():
    print("Set keyboard light level for MacBook Pro laptops")
    print(" ")
    print("Options:")
    print(" -v          : verbose")
    print("Usage:")
    print("   mbpklc <option> up/down")
    print(" ex.: ")
    print("   mbpklc up   : increases the keyboard backlight")
    print("   mbpklc down : decreases the keyboard backlight")
    print("   mbpklc off  : turns off the keyboard backlight")


def get_kbd_light_level():
    with open(os.path.join(BLPATH, BLVALFILE), 'r') as myfile:
        data = myfile.read().replace('\n', '')
        return int(data)


def get_max_kbd_light_level():
    with open(os.path.join(BLPATH, BLMAXFILE), 'r') as myfile:
        data = myfile.read().replace('\n', '')
        return int(data)


def set_kbd_light_level(lvl, verbose=False):
    max_value = get_max_kbd_light_level()
    unit = (max_value // 100) * 10  # int division

    new_value = -1

    if lvl == "up":
        new_value = get_kbd_light_level()
        if new_value + unit < max_value:
            new_value += unit
        else:
            new_value = max_value
        if verbose:
            print("Increased to {} of max {} (+{})".format(new_value, max_value, unit))
    elif lvl == "down":
        new_value = get_kbd_light_level()
        if new_value - unit > unit:
            new_value -= unit
        else:
            new_value = 0
        if verbose:
            print("Decreased to {} of max {} (-{})".format(new_value, max_value, unit))
    elif lvl == "off":
        new_value = 0
        if verbose:
            print("Decreased to {} of max {} (-{})".format(new_value, max_value, unit))

    if new_value != -1:
        file = open(os.path.join(BLPATH, BLVALFILE), 'w')
        file.write(str(new_value))
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1].strip() == "up" or sys.argv[1].strip() == "down" or sys.argv[1].strip() == "off":
            set_kbd_light_level(sys.argv[1].strip())
        else:
            print("Unknown command : {}".format(sys.argv[1]))

    elif len(sys.argv) == 3 and sys.argv[1] == "-v":
        if sys.argv[2].strip() == "up" or sys.argv[2].strip() == "down" or sys.argv[2].strip() == "off":
            set_kbd_light_level(sys.argv[2].strip(), verbose=True)
        else:
            print("Unknown command : {}".format(sys.argv[2]))
    else:
        help()
