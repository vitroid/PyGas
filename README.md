# PyGas

PyGas is a collection of molecular dynamics simulation codes for demonstration written in Python.

## Environment

[Anaconda](https://www.anaconda.com) is recommended.

## Requirement

Install the following packages in advance. They are available via `pip` package manager.

* Numpy
* pygame

`ffmpeg` is required to record the video.

## Files

### `harddisk.py`: Hard disks or hard spheres.

    pygame 2.1.2 (SDL 2.0.18, Python 3.9.10)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    usage: harddisk.py [-h] [--version] [--atoms 32] [--record 32] [--dt 0.1]
                       [--temp 1.0] [--cell 10,10] [--hist] [--flight]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --record 32, -r 32    Record the first x frames in a mp4 file.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --flight, -f          Output time-of-flight infos.


### `LennardJones.py`: Lennard-Jones gas.

    pygame 2.1.2 (SDL 2.0.18, Python 3.9.10)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    usage: LennardJones.py [-h] [--version] [--atoms 32] [--vel 1] [--dt 0.1]
                           [--temp 1.0] [--cell 10,10] [--hist] [--debug]
                           [--quiet]
                           [basename]
    
    Molecular dynamics of Lennard-Jones gas. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --vel 1, -v 1         Output velocity list every i steps.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --debug, -D           Show debug messages.
      --quiet, -Q           Suppress messages.


----

# PyGas

PyGasはlPythonで書かれた気体分子運動のデモ用の分子動力学プログラムです。

## 環境

[Anaconda](https://www.anaconda.com)のPython環境を推奨します。

## 必要なもの

以下のパッケージをあらかじめインストールして下さい。これらは`pip`でインストールできます。

* Numpy
* pygame

## ファイル

### `harddisk.py`: 剛体円盤、剛体球のシミュレーション。

    pygame 2.1.2 (SDL 2.0.18, Python 3.9.10)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    usage: harddisk.py [-h] [--version] [--atoms 32] [--record 32] [--dt 0.1]
                       [--temp 1.0] [--cell 10,10] [--hist] [--flight]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --record 32, -r 32    Record the first x frames in a mp4 file.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --flight, -f          Output time-of-flight infos.


### `LennardJones.py`: Lennard-Jonesガスのシミュレーション。

    pygame 2.1.2 (SDL 2.0.18, Python 3.9.10)
    Hello from the pygame community. https://www.pygame.org/contribute.html
    usage: LennardJones.py [-h] [--version] [--atoms 32] [--vel 1] [--dt 0.1]
                           [--temp 1.0] [--cell 10,10] [--hist] [--debug]
                           [--quiet]
                           [basename]
    
    Molecular dynamics of Lennard-Jones gas. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --vel 1, -v 1         Output velocity list every i steps.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --debug, -D           Show debug messages.
      --quiet, -Q           Suppress messages.

