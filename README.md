# WinApt

<img src="misc/cube.png" align="right" width="200" height="200"/>

_The simple package installer for Windows_

[![License](https://img.shields.io/badge/license-GPL%203.0-blue.svg?style=flat)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-blue.svg?style=flat)](#)

---

WinApt is a simple program which automates software installation on Windows. It tries to
do one simple thing and do it well: download a `setup.exe` and install it, silently.

## Instructions
To install a package, for example Firefox, run:

    winapt firefox

There are also other commands and flags that are described in the output of `winapt -help`.

## Development

To contribute a new package, see
[here](misc/registry.md).

To work on WinApt itself you will need Git and the Python compiler. You can
install them with WinApt itself:

    winapt git python


## Credits

The cube icon is derived from the one available from [Flaticon](https://flaticon.com/).
