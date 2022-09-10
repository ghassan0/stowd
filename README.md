# doti

Easily manage all your dotfiles across your devices.

## Motivation

I wanted a simple way to manage all [my dotfiles](https://github.com/ghassan0/dotfiles) while having each application isolated so I can easily share them across different devices.

Popular options:

- `stow` - great simple tool but a hassle to manage multiple separate dotfiles
- `chezmoi` - powerful tool but I didn't want the complexity that came with it

I created `doti` to fill the gap between `stow` and `chezmoi`.
It utilizes `stow` and a config file to manage dotfiles of multiple programs on different systems.

## Features

Features:

- Isolate all configs of an application into its own directory.
- Use same directory structure as can be seen from the `home` (`~`) or `root` (`/`) directories within the application's own directory.
- Symlink configs so we can edit directly from the dotfiles directory instead of trying to hunt the config files down.
- Both `home` and `root` configs supported.
- Hostname-specific, system-specific, and general configs
- Supports Linux, Termux, OSX, OpenBSD, FreeBSD, and Cygwin.
- Non-root installation using `pip`.

Non-features:

- No template files. I want the configs to be portable and not rely on `doti` or any specific dotfile manager.

## Installation

Requirements: `stow`

```
# Cross-Platform (pip)
pip install doti

# or

# Arch Linux (AUR)
yay -S doti
```

## Setup

Within the dotfiles directory, create a separate sub-directory for each program.
Within each sub-directory organize that programs config files as they appear from the home or root directory.

<details>
  <summary>Example dotfiles directory structure:</summary>

```
.
├── doti
│   └── .config
│       └── doti
│           └── doti.cfg
├── dircolors
│   └── .config
│       └── dircolors
│           └── .dir_colors
├── env_root
│   └── etc
│       └── environment
├── git
│   └── .config
│       └── git
│           └── config
├── gtk
│   └── .config
│       ├── gtk-2.0
│       │   └── gtkrc
│       └── gtk-3.0
│           ├── gtk.css
│           └── settings.ini
├── termux
│   └── .termux
│       ├── colors.properties
│       └── termux.properties
├── tty
│   └── etc
│       ├── issue
│       └── profile
└── zsh
    ├── .config
    │   └── zsh
    │       ├── .zprofile
    │       └── .zshrc
    └── .zshenv
```

</details>

## Configuration

Check the sample [doti.cfg](sample/doti.cfg) file for details.

## Usage

Run `doti` without arguments to use all the settings from the config file.

<details>
  <summary>doti -h</summary>

```
usage: doti [-h] [-s NAME [NAME ...]] [-S NAME [NAME ...]]
             [-u NAME [NAME ...]] [-U NAME [NAME ...]] [-r] [-R] [-c FILE]
             [-d DIR] [-v] [-q] [-n] [-V]
             [NAME ...]

Symlink dotfiles into their respective directories using `stow`.

positional arguments:
  NAME                  stow dir[s] to the home directory

options:
  -h, --help            show this help message and exit
  -s NAME [NAME ...], --stow NAME [NAME ...]
                        stow dir[s] to the home directory
  -S NAME [NAME ...], --stow-root NAME [NAME ...]
                        stow dir[s] to the root directory
  -u NAME [NAME ...], --unstow NAME [NAME ...]
                        unstow dir[s] from the home directory
  -U NAME [NAME ...], --unstow-root NAME [NAME ...]
                        unstow dir[s] from the root directory
  -r, --root-enable     enable root section in config
  -R, --root-only       only use root section in config
  -c FILE, --config FILE
                        path to config file (doti.cfg)
  -d DIR, --dotfiles DIR
                        path to dotfiles directory
  -v, --verbose         show verbose output
  -q, --quiet           supress output
  -n, --no, --simulate  simulate run, no filesystem modification
  -V, --version         show version number
```

</details>
