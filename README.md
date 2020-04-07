# A virtual game of Hanabi in Python

This project started is a hobby and a pet project to practice collaboration in GitHub, using a GUI, communication over the network etc. It is not (yet) published as a package and it isn't tested (yet).


## Installation instructions

Open a terminal and navigate to the installation directory:

```
cd Documents/somewhere/I/like
```

Clone the repo and move into it:

```
git clone https://github.com/rodrigolece/hanabi.git
cd hanabi
```

Install the dependencies using:

```
python3 -m pip install -r requirements.txt
```

### Optional, use a conda environment

We strongly recommend that you use a conda environment. Assuming that either Anaconda or minicoda (❤️) is installed (instructions for the latter for [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) or [macOS](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)).

The game was tested with Python 3.7, so below we create an environment called `hanabi` and we activate it (switch to using the correct version of python):

```
conda create -y -n hanabi python=3.7
conda activate hanabi
```

Run this step **before** the `pip install` command.

## Run

Assuming that a server is listening, run:

```
./main.py
```
