# Pytris

This is on open source game similar to everyone's favorite. The original work came from @rledford(@exsolacyst). The code has been refactored, with some minor bells and whistles added for modern gameplay. This will continue to be expanded to make a strong base for anyone interested in generating a custom clone.

## Install

Right now the platform of support is limited to Debian-like systems. To install just do the following:

```
sudo apt-get install python-pygame
git clone https://github.com/raymondberg/pytetris.git
cd pytetris
python run.py
```

## Configuration

Most of the configs are stored in `pytris/config.py`. Play around at your own risk!


## Release Notes

* 2.0.0 - A complete refactor of the underlying code.
  * Now pytris is a package that can be imported and run any number of ways; the simplest way is documented in `run.py`.
  * This release supports multiple game-runs from a single python instance.
  * Additionally, support for the Buffalo USB Game pad added.

* 1.3.0 - The initial version loaded from Google projects source code. Invoke by calling `python Clone_of_Tetris.py`.
