#!/usr/bin/env python -u

# lj2.py + numpy

import argparse as ap
import random as ra
import sys
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger
from math import *

import numpy as np

from histogram import Hist
from nodebox_wrapper import *

__version__ = "0.1"


# General list serializer

def serialize(x):
    dim = len(x)
    s = ""
    for i in range(0, dim):
        s += "%s " % x[i]
    s += "\n"
    return s

# General list unserializer


def unserialize(s):
    s = s.rstrip(" \n")
    x = s.split(" ")
    for i in range(0, len(x)):
        x[i] = float(x[i])
    return x

#graphic context #######################################################


class GC:
    def __init__(self, zoom=1.0):
        self.zoom = zoom


#a set of LJ particles ########################################################
class Particles:
    def __init__(self, pos=None, vel=None, file=None):
        if file is not None:
            self.load(file)
        else:
            self.pos = pos
            self.vel = vel
            self.resetforce()
            self.N, self.dim = pos.shape

    def forward(self, dt):
        self.pos += self.vel * dt

    def accel(self, dt):
        self.vel += self.force * dt

    def resetforce(self):
        self.force = np.zeros_like(self.pos)

    def rescale(self, factor):
        self.vel *= factor

    def interact(self, cell):
        posx = np.broadcast_to(
            self.pos,
            (self.pos.shape[0],
             self.pos.shape[0],
             self.pos.shape[1]))
        posy = np.swapaxes(posx, 0, 1)
        delta = posx - posy
        delta -= np.floor(delta / cell + 0.5) * cell
        ddsum = np.sum(delta * delta, axis=2)
        pot = 4.0 * (ddsum**-6 - ddsum**-3)
        force0 = -48.0 * ddsum**-7 + 24.0 * ddsum**-4
        pot[np.isnan(pot)] = 0.0
        force0[np.isnan(force0)] = 0.0
        virial = force0 * ddsum
        force = np.zeros_like(self.pos)
        for d in range(self.dim):
            force[:, d] -= np.sum(force0 * delta[:, :, d], axis=0)
            force[:, d] += np.sum(force0 * delta[:, :, d], axis=1)
        self.force = force
        return np.sum(pot) / 2.0, np.sum(virial) / 2.0

    def kinetic(self):
        return 0.5 * np.sum(self.vel**2)

    def randomize(self, kt):
        v = 4.0 * kt
        self.vel = v * (np.random.random(self.pos.shape) - 0.5)

    def draw(self, cell, gc, avgvel):
        pos = self.pos.copy()
        pos -= np.floor(pos / cell) * cell
        if self.dim < 3:
            for p, v in zip(pos, self.vel):
                oval((p[0] - 0.5) * gc.zoom, (p[1] - 0.5)
                     * gc.zoom, gc.zoom, gc.zoom)
                line(
                    p[0] * gc.zoom,
                    p[1] * gc.zoom,
                    (p[0] + v[0]) * gc.zoom,
                    (p[1] + v[1]) * gc.zoom)
        else:
            for i in sorted(range(pos.shape[0]), key=lambda x: pos[x, 2]):
                p = pos[i]
                v = self.vel[i]
                speed = np.linalg.norm(v)
                sat = (p[2] / cell[2]) * 0.5 + 0.5
                hue = 0.666 - 0.3 * speed / avgvel
                fill(hue, 1.0, sat, 0.8)
                a = 0.5 / speed
                b = a + 1.0
                if v[2] >= 0.0:
                    oval((p[0] - 0.5) * gc.zoom, (p[1] - 0.5)
                         * gc.zoom, gc.zoom, gc.zoom)
                line((p[0] + v[0] * a) * gc.zoom, (p[1] + v[1] * a) * gc.zoom,
                     (p[0] + v[0] * b) * gc.zoom, (p[1] + v[1] * b) * gc.zoom)
                if v[2] < 0.0:
                    oval((p[0] - 0.5) * gc.zoom, (p[1] - 0.5)
                         * gc.zoom, gc.zoom, gc.zoom)

    # serialize
    def __str__(self):
        # + serialize(self.force)
        s = serialize(self.pos) + serialize(self.vel)
        return s

    def load(self, file):
        s = file.readline()
        self.pos = unserialize(s)
        s = file.readline()
        self.vel = unserialize(s)
        #s = file.readline()
        #self.force = unserialize(s)
        s = file.readline()
        self.force = [0.0] * len(self.pos)

    def save(self, file):
        file.write("%s\n" % self)


def lattice1d(nballs):
    n = nballs
    gap = 0.02
    ex = 1 + gap
    x = 0.0
    pos = []
    while 0 < n:
        pos.append([x])
        n -= 1
        x += ex
    pos = np.array(pos)
    vel = np.zeros_like(pos)
    return Particles(pos, vel)


def lattice2d(nballs, cell):
    logger = getLogger()
    n = nballs
    gap = 0.02
    ex = 1 + gap
    nx = int(cell[0] / ex)
    ny = int(cell[1] / (ex * sqrt(3.0) / 2))
    pos = []
    for iy in range(0, ny):
        for ix in range(0, nx):
            x = ix * ex
            y = iy * ex * sqrt(3.0) / 2 + 0.1
            if iy % 2 != 0:
                x += ex / 2.0
            pos.append([x, y])
            n -= 1
            if n == 0:
                break
        if n == 0:
            break
    pos = np.array(pos)
    vel = np.zeros_like(pos)
    if pos.shape[0] < nballs:
        logger.info("Placed only {0} particles.".format(pos.shape[0]))
    return Particles(pos, vel)


def lattice3d(nballs, cell):
    logger = getLogger()
    n = nballs
    gap = 0.02
    ex = 1 + gap
    nx = int(cell[0] / ex)
    ny = int(cell[1] / (ex * sqrt(3.0) / 2))
    nz = int(cell[2] / (ex * sqrt(6.0) / 3.0))
    pos = []
    for iz in range(0, nz):
        for iy in range(0, ny):
            for ix in range(0, nx):
                x = ix * ex
                y = iy * ex * sqrt(3.0) / 2 + 0.1
                z = iz * ex * sqrt(6.0) / 3 + 0.1
                if iy % 2 != 0:
                    x += ex / 2.0
                if iz % 2 != 0:
                    x += ex / 2.0
                    y += ex * sqrt(3.0) / 2 * 2.0 / 3.0
                pos.append([x, y, z])
                n -= 1
                if n == 0:
                    break
            if n == 0:
                break
        if n == 0:
            break
    pos = np.array(pos)
    vel = np.zeros_like(pos)
    if pos.shape[0] < nballs:
        logger.info("Placed only {0} particles.".format(pos.shape[0]))
    return Particles(pos, vel)


def lattice(nballs, cell):
    dim = cell.shape[0]
    if dim == 1:
        return lattice1d(nballs)
    elif dim == 2:
        return lattice2d(nballs, cell)
    elif dim == 3:
        return lattice3d(nballs, cell)

#System of particles ###################################################


class System:
    def __init__(self,
                 cell=None,
                 nballs=10,
                 step=0,
                 gc=None,
                 input=None,
                 logfile=sys.stdout,
                 velfile=None,
                 velint=0,
                 kT=None,
                 hist=False):
        self.cell = cell
        if input is not None:
            self.load(input)
        else:
            self.balls = lattice(nballs, cell)
            if kT is not None:
                # ra.seed(1)
                self.thermalize(kT)
        self.balls.interact(cell)
        self.step = step
        self.gc = gc
        self.logfile = logfile
        self.velfile = velfile
        self.velinterval = velint
        self.kT = kT
        self.hist = hist
        self.histx = Hist(-5, +5, 0.05)
        self.histy = Hist(-5, +5, 0.05)

    def thermalize(self, kT):
        self.balls.randomize(kT)
        # Remove total translation
        velsum = np.sum(self.balls.vel, axis=0)
        velsum /= self.balls.N
        self.balls.vel -= velsum

    def OneStep(self, dt):
        # Progress Momenta (half)
        self.balls.accel(dt / 2.0)
        # Progress Position
        self.balls.forward(dt)
        self.balls.resetforce()
        # Force
        self.pot, virsum = self.balls.interact(self.cell)
        # Progress Momenta (half)
        self.balls.accel(dt / 2.0)
        # temperature scaling
        # if self.kT is not None:
        if False:
            kin = self.balls.kinetic()
            dof = self.balls.N * self.cell.shape[0]
            factor = (self.kT * dof / 2.0) / kin
            factor = 1.0 - (1.0 - factor) * 0.001
            self.balls.rescale(factor)
        # Data output
        if self.logfile is not None:
            dof = self.balls.dim * self.balls.N
            kin = self.balls.kinetic()
            kT = 2.0 * kin / dof
            z = 1.0 - virsum / (dof * kT)
            self.logfile.write(
                "%s %s %s %s %s %s\n" %
                (self.step, kT, z, kin + self.pot, kin, self.pot))
        if self.velfile is not None and self.step % self.velinterval == 0:
            for i in range(0, N):
                self.velfile.write("%s\n" %
                                   sqrt(2.0 * self.balls[i].kinetic()))
        # histogram
        for v in self.balls.vel:
            self.histx.accum(v[0], 1.0)
            if len(v.shape) > 1:
                self.histy.accum(v[1], 1.0)
        self.step += 1

    def draw(self):
        if self.gc is not None:
            dim = self.cell.shape[0]
            if 2 < dim:
                avgvel = 1.0
                if self.kT is not None:
                    avgvel = sqrt(dim * self.kT)
                self.balls.draw(self.cell, self.gc, avgvel)
            else:
                self.balls.draw(self.cell, self.gc, 0.0)
            if dim > 1:
                canvasx = self.cell[0] * self.gc.zoom
                canvasy = self.cell[1] * self.gc.zoom
                if self.hist:
                    self.histx.draw(0, canvasy, canvasx, canvasy / 2)
                    self.histx.draw(
                        canvasx,
                        canvasy,
                        canvasx / 2,
                        canvasy,
                        vertical=True)
            else:
                canvasx = self.cell[0] * self.gc.zoom
                canvasy = self.gc.zoom
                if self.hist:
                    self.histx.draw(0, canvasy, canvasx, canvasy / 2)
#                    self.histx.draw(canvasx,canvasy,canvasx/2,canvasy,vertical=True)

    def load(self, file):
        self.balls = []
        s = file.readline()
        self.cell = unserialize(s)
        s = file.readline()
        x = unserialize(s)
        x = int(x[0])
        for i in range(0, x):
            self.balls.append(Particle(file=file))
        s = file.readline()

    # serialize
    def __str__(self):
        s = serialize(self.cell)
        s += "%s\n" % len(self.balls)
        for i in range(0, len(self.balls)):
            s += "%s\n" % self.balls[i]
        return s

    def save(self, file):
        file.write("%s\n" % self)


#Commandline parser #########################################################
def getoptions():
    parser = ap.ArgumentParser(
        description='Molecular dynamics of Lennard-Jones gas. (version {0})'.format(__version__),
        prog='LennardJones.py')
    parser.add_argument('--version',
                        '-V',
                        action='version',
                        version='%(prog)s {0}'.format(__version__))
    parser.add_argument('--atoms',
                        '-a',
                        type=int,
                        dest='atoms',
                        metavar="32",
                        default=32,
                        help='Specify number of atoms.')
    parser.add_argument('--vel',
                        '-v',
                        type=float,
                        dest='velinterval',
                        metavar="1",
                        help='Output velocity list every i steps.')
    parser.add_argument('--dt',
                        '-d',
                        type=float,
                        dest='dt',
                        metavar="0.1",
                        default=0.1,
                        help='Step interval.')
    parser.add_argument('--temp',
                        '-t',
                        type=float,
                        dest='temp',
                        metavar="1.0",
                        default=1.0,
                        help='Specify the initial temperature in kT.')
    parser.add_argument('--cell',
                        '-c',
                        dest='cell',
                        metavar="10,10",
                        default="10,10",
                        help='Specify the cell shape.')
    parser.add_argument('--hist',
                        '-H',
                        action='store_true',
                        dest='hist',
                        help='Show velocity histograms.')
    parser.add_argument('--debug',
                        '-D',
                        action='store_true',
                        dest='debug',
                        help='Show debug messages.')
    parser.add_argument('--quiet',
                        '-Q',
                        action='store_true',
                        dest='quiet',
                        help='Suppress messages.')
    parser.add_argument('basename',
                        nargs='?',
                        help='Basename of the output file.')
    return parser.parse_args()


#For nodebox animation #################################################


def setup():
    global system, options
    zoom = 60.0
    #コマンドラインオプションの解析 ####################################
    options = getoptions()
    # Logger
    if options.debug:
        basicConfig(level=DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s")
    elif options.quiet:
        basicConfig(level=WARNING,
                            format="%(levelname)s %(message)s")
    else:
        # normal
        basicConfig(level=INFO,
                            format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    #Initialize ########################################################
    velfile = None
    logfile = None
    if options.basename is not None:
        logfilename = "%s.log" % options.basename
        logfile = open(logfilename, "w")
        if options.velinterval is not None:
            velfilename = "%s.vel" % options.basename
            velfile = open(velfilename, "w")
    cell = np.array([float(x) for x in options.cell.split(",")])
    system = System(nballs=options.atoms,
                    cell=cell,
                    gc=GC(zoom=zoom),
                    logfile=logfile,
                    velfile=velfile,
                    velint=options.velinterval,
                    hist=options.hist,
                    kT=options.temp)
    # for NodeBox-like action
    if len(cell) == 1:
        size(zoom * cell[0], zoom)
    else:
        size(zoom * cell[0], zoom * cell[1])


def draw():
    global system, options
    colormode(HSB)
    stroke(0, 0, 0)
    fill(0, 0, 1)
    for i in range(10):
        system.OneStep(options.dt / 10)
    system.draw()


speed(100)
animate(setup, draw)
