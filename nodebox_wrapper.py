#!/usr/bin/env python
# coding: utf-8

#
# 2020 video recording
#

import pygame
from pygame.locals import *
import random as ra
import logging
import subprocess
from logging import getLogger

# settings
RGB = "rgb"
HSB = "hsb"
COLORMODE = RGB
STROKECOLOR = Color(0, 0, 0, 255)
FILLCOLOR = Color(100, 100, 100, 255)
BACKGROUND = Color(255, 255, 255, 255)
FILL = True
STROKE = False
STROKEWIDTH = 1
FPS = 0
FRAME = 0
WIDTH = 0
HEIGHT = 0
MOUSEX = 1
MOUSEY = 2
mousedown = False
keydown = False
key = ""

# initialize anyway
pygame.init()


# define the campus size
def size(w, h):
    global SCREEN, WIDTH, HEIGHT
    logger = logging.getLogger()
    logger.debug("size {0} {1}".format(w, h))
    WIDTH = w
    HEIGHT = h
    SCREEN = pygame.display.set_mode((int(w), int(h)), 0, 24)
    SCREEN.fill(BACKGROUND)
    pygame.display.flip()  # 裏画面に描かれたものを表示する。


def colormode(mode):
    global COLORMODE
    COLORMODE = mode

# set the line color
# value range: 255,255,255 for pygame RGB
# 360,100,100,100 for pygame hsva


def stroke(A, B=999, C=999, D=0.5):
    global STROKECOLOR, STROKE
    STROKE = True
    if B == 999:
        B = A
        C = A
    if A > 1:
        A = 1
    if B > 1:
        B = 1
    if C > 1:
        C = 1
    if COLORMODE == RGB:
        STROKECOLOR = (A * 255, B * 255, C * 255)
    elif COLORMODE == HSB:
        STROKECOLOR.hsva = (A * 360, B * 100, C * 100, D * 100)


def nostroke():
    global STROKE
    STROKE = False


def nofill():
    global FILL
    FILL = False

# set the fill color


def fill(A, B=999, C=999, D=1):
    global FILLCOLOR, FILL
    FILL = True
    if isinstance(A, list) or isinstance(A, tuple):
        A, B, C, D = A
    if B == 999:
        B = A
        C = A
    if A > 1:
        A = 1
    if B > 1:
        B = 1
    if C > 1:
        C = 1
    if A < 0:
        A = 0
    if COLORMODE == RGB:
        FILLCOLOR = Color(A * 255, B * 255, C * 255, D * 255)
    elif COLORMODE == HSB:
        FILLCOLOR.hsva = (A * 360, B * 100, C * 100, D * 100)


def oval(x, y, w, h):
    if FILL:
        pygame.draw.ellipse(SCREEN, FILLCOLOR, (x, y, w, h))
    if STROKE:
        pygame.draw.ellipse(SCREEN, STROKECOLOR, (x, y, w, h), STROKEWIDTH)


def rect(x, y, w, h):
    if FILL:
        pygame.draw.rect(SCREEN, FILLCOLOR, (x, y, w, h))
    if STROKE:
        pygame.draw.rect(SCREEN, STROKECOLOR, (x, y, w, h), STROKEWIDTH)


def line(x1, y1, x2, y2):
    if STROKE:
        pygame.draw.line(SCREEN, STROKECOLOR, [x1, y1], [x2, y2], STROKEWIDTH)


def random():
    return ra.random()


def strokewidth(w):
    global STROKEWIDTH
    STROKEWIDTH = int(w + 0.5)


def speed(fps):
    global FPS
    FPS = fps


def animate(setup, draw, video=0):
    global FPS, FRAME, MOUSEX, MOUSEY, WIDTH, HEIGHT, SCREEN, mousedown, keydown, key
    logger = getLogger()
    setup()
    if FPS == 0:
        draw()
        return
    if video > 0:
        # setup video
        pcmd = ["ffmpeg",
                "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", "{0}x{1}".format(int(WIDTH), int(HEIGHT)),
                "-pix_fmt", "rgb24",
                "-r", "{0}".format(FPS),
                "-i", "-",
                "-an",
                "-pix_fmt",
                "yuv420p",
                "nodebox.mp4"]
        pipe = subprocess.Popen(
            pcmd,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE)
    while True:
        events = pygame.event.get()
        # logger.debug(events)
        keydown = False
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                keydown = True
                key = ev.unicode
        # pressed = pygame.key.get_pressed()
        if key == "q":  # pressed[K_q]:
            break
        MOUSEX, MOUSEY = pygame.mouse.get_pos()
        mousedown = pygame.mouse.get_pressed()[0]  # left button
        SCREEN.fill(BACKGROUND)
        draw()
        pygame.display.flip()  # 裏画面に描かれたものを表示する。
        pygame.time.wait(1000 // FPS)
        FRAME += 1
        if video > 0:
            s = pygame.image.tostring(SCREEN, "RGB", False)
            # print(len(s))
            pipe.stdin.write(s)
        if video == FRAME:
            break
    if video > 0:
        # pipe.close()
        pass


# quick hack
def beginpath(x, y):
    global _points
    _points = [(x, y)]


def lineto(x, y):
    global _points
    _points.append((x, y))


def endpath():
    global _points
    # unfortunately, there is no easy way to alpha-blend it with pygame.
    if FILL:
        pygame.draw.polygon(SCREEN, FILLCOLOR, _points, width=0)
    if STROKE:
        pygame.draw.polygon(SCREEN, STROKECOLOR, _points, width=STROKEWIDTH)


# just deny it for now
def text(s, x, y):
    pass


def setup():
    # default setup()
    size(500, 500)


def wait_q():
    pygame.display.flip()  # 裏画面に描かれたものを表示する。
    while True:
        pygame.event.get()
        pressed = pygame.key.get_pressed()
        if pressed[K_q]:
            break
        pygame.time.wait(100)


def color(A, B, C, D):
    return A, B, C, D
