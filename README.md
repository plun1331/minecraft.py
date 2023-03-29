# minecraft.py

A simple Minecraft client wrapper for Python 3.10+.

**This project is currently in a very early stage.** 
It is not recommended to use this in production, 
as there are many bugs and missing features.


## Installing

**Only Python 3.10+ is supported.** This has not been tested on lower versions.

### Stable (none)

There is no stable version yet.

### Alpha (0.0.0a1)

You can install the alpha version from GitHub:

```bash
$ git clone https://github.com/plun1331/minecraft.py
$ cd minecraft.py
$ python3 -m pip install -U .[microsoft-auth]
```

or if you do not want to clone the repository:

```bash
$ python3 -m pip install -U git+https://github.com/plun1331/minecraft.py
```

Note that this requires that you have [`git`](https://git-scm.com/) installed.


### Optional Requirements
- `microsoft-auth`
    - [`msal`](https://pypi.org/project/msal/) for Microsoft authentication
- `docs`
    - [`sphinx`](https://pypi.org/project/sphinx/) for documentation generation.
    - [`furo`](https://pypi.org/project/furo/) for our documentation styling.
    - [`myst-parser`](https://pypi.org/project/myst-parser/) for parsing markdown files.
