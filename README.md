# WinApt

<img src="https://cdn-icons-png.flaticon.com/512/645/645928.png" align="right" width="200" height="200"/>

_The simple package installer for Windows_

[![License](https://img.shields.io/badge/license-GPL%203.0-blue.svg?style=flat)]((#))
[![Semver](https://img.shields.io/badge/version-v0.1-blue.svg?style=flat)]((#))

---

WinApt is a simple program which automates software installation on Windows. It tries to
do one simple thing and do it well: download a `setup.exe` and install it, silently.

## Instructions
To install a package, for example Firefox, run:

    winapt firefox

There are also other commands and flags that are described in the output of `winapt -help`.

## Development

To contribute a new package, see
[here](https://github.com/just-install/registry/blob/master/README.md).

To work on just-install itself you will need Git and the Python compiler. You can
install them with WinApt itself:

    winapt git python


## Credits

The cube icon is derived from the one available from [Ionicons](https://ionicons.com/).
