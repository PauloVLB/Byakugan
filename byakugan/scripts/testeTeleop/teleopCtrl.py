#!/usr/bin/env python
# -*- conding: utf8 -*-

import rospy
import curses
import os
from . import Motores

def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr("Detected key:")
    while not rospy.is_shutdown():
        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           keyPressed = str(key)
           if keyPressed == "KEY_UP":
               win.addstr("Em frente")
               #motores.roboEmFrente()
           elif keyPressed == "KEY_DOWN":
               win.addstr("Para tras")
               #motores.roboEmFrente()
           elif keyPressed == "KEY_LEFT":
               win.addstr("Para esquerda")
               #motores.roboEmFrente()
           elif keyPressed == "KEY_RIGHT":
               win.addstr("Para direita")
               #motores.roboEmFrente()
           if key == os.linesep:
              break
        except Exception as e:
           # No input
           pass

if __name__ == "__main__":
    # motores = Motores('pubTeleopMotores')
    curses.wrapper(main)
