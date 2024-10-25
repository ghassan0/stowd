# doti

Easily manage all your dotfiles across your devices.

## Motivation

I wanted a simple way to manage all [my dotfiles](https://github.com/alduraibi/dotfiles) while having each application isolated, so I can easily share them across different devices.

Popular options:

- `stow` - great simple tool but a hassle to manage multiple separate dotfiles
- `chezmoi` - powerful tool but I didn't want the complexity that came with it

I created `doti` to extend the functionality, simplicity, and portability of `stow` with a config file to manage dotfiles of multiple programs on different systems.

## Features

Features:

- Isolate all configs of an application into its own directory.
- Use same directory structure as can be seen from the `home` (`~`) or `root` (`/`) directories within the application's own directory.
- Symlink configs so we can edit directly from the dotfiles directory instead of trying to hunt the config files down.
- Both `home` and `root` configs supported.
- Hostname-specific, distro-specific, system-specific, and general configs
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

# Cross-Platform (pip with venv) [recommended over just pip]
cd ~/.dotfiles                # cd into your dotfiles directory
python -m venv .venv          # create python virtual environent
source .venv/bin/activate     # activate venv
python -m pip install doti    # install doti

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
│   └── doti.cfg
├── bat
│   └── .config
│       └── bat
│           └── config
├── dircolors
│   └── .config
│       └── dircolors
│           └── .dir_colors
├── electron
│   └── .config
│       └── electron-flags.conf
├── env_root
│   └── etc
│       └── environment
├── git
│   └── .config
│       └── git
│           ├── config
│           └── ignore
├── gtk
│   └── .config
│       ├── gtk-2.0
│       │   └── gtkrc
│       └── gtk-3.0
│           ├── gtk.css
│           └── settings.ini
├── neovim
│   └── .config
│       └── nvim
│           └── init.lua
├── termux
│   └── .termux
│       ├── colors.properties
│       └── termux.properties
├── pacman
│   └── etc
│       ├── issue
│       └── pacman.conf
├── tmux
│   └── .config
│       └── tmux.conf
├── vim
│   └── .vimrc
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
usage: doti [-h] [-r] [-R] [-c FILE] [-d DIR] [-v] [-q] [-n] [-V]
            {add,remove} ...

Symlink dotfiles into their respective directories using `stow`.

positional arguments:
  {add,remove}

options:
  -h, --help            show this help message and exit
  -r, --root-disable    disable root section in config
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

<details>
  <summary>doti add -h</summary>

```
usage: doti add [-h] [-r] NAME [NAME ...]

positional arguments:
  NAME        symlink dir[s]'s files to the home directory

options:
  -h, --help  show this help message and exit
  -r, --root  use root dir instead of home
```

</details>

</details>

<details>
  <summary>doti remove -h</summary>

```
usage: doti remove [-h] [-r] NAME [NAME ...]

positional arguments:
  NAME        remove dir[s]'s symlinks from the home directory

options:
  -h, --help  show this help message and exit
  -r, --root  use root dir instead of home
```

</details>
