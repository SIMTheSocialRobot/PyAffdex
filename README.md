# PyAffdex

Python library for accessing the Affectiva Emotion SDK (Affdex)

## Installation

**You must install the [Affdex SDK](http://developer.affectiva.com/index.html) before using this module.**

Installation and usage of the Affdex SDK is subject to the terms put forth by Affectiva.

## Requirements

_TBD_

## Usage

`import PyAffdex`

Refer to the _examples_ folder for full example programs.

## Supported Systems

* OS X 10.10 (Yosemite)

## Tested Combinations

| System     | Python |Affdex Version |
|------------|--------|---------------|
| OS X 10.10 | 3.5    |3.1.1          |

_This library is **incompatible with Python 2.**_

## Limitations

**This library cannot process video files nor live feeds from a camera**. It can, however, process consecutive frames extracted from a video, as well as single images.

## Legal

This module is in no way endorsed by Affectiva, nor does it claim to be.

The `PyAffdex` module is released under the BSD License. Full language of the license is available in [LICENSE.md](LICENSE.md)
