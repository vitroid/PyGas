# PyGas

PyGas is a collection of molecular dynamics simulation codes for demonstration written in Python.

## Environment

[Anaconda](https://www.anaconda.com) is recommended.

## Requirement

Install the following packages in advance. They are available via `pip` package manager.

* Numpy
* pygame

## Files

### `harddisk.py`: Hard disks or hard spheres.

    usage: harddisk.py [-h] [--version] [--atoms 32] [--dt 0.1] [--temp 1.0]
                       [--cell 10,10] [--hist] [--flight]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --flight, -f          Output time-of-flight infos.


### `LennardJones.py`: Lennard-Jones gas.

    usage: harddisk.py [-h] [--version] [--atoms 32] [--vel 1] [--dt 0.01]
                       [--temp 1.0] [--cell 10,10] [--hist]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --vel 1, -v 1         Output velocity list every i steps.
      --dt 0.01, -d 0.01    Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.


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

    usage: harddisk.py [-h] [--version] [--atoms 32] [--dt 0.1] [--temp 1.0]
                       [--cell 10,10] [--hist] [--flight]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --dt 0.1, -d 0.1      Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.
      --flight, -f          Output time-of-flight infos.


### `LennardJones.py`: Lennard-Jonesガスのシミュレーション。

    usage: harddisk.py [-h] [--version] [--atoms 32] [--vel 1] [--dt 0.01]
                       [--temp 1.0] [--cell 10,10] [--hist]
                       [basename]
    
    Molecular dynamics of hard spheres. (version 0.1)
    
    positional arguments:
      basename              Basename of the output file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --atoms 32, -a 32     Specify number of atoms.
      --vel 1, -v 1         Output velocity list every i steps.
      --dt 0.01, -d 0.01    Step interval.
      --temp 1.0, -t 1.0    Specify the initial temperature in kT.
      --cell 10,10, -c 10,10
                            Specify the cell shape.
      --hist, -H            Show velocity histograms.

