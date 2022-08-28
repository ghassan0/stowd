# stowd

Easily manage all your dotfiles across your devices.

## Motivation

I wanted a simple way to manage all my dotfiles and share them across different devices.

Popular options:

- `stow` - great simple tool but a hassle to manage multiple separate dotfiles
- `chezmoi` - powerful tool but I didn't want the complexity that came with it

I created `stowd` to fill the gap between `stow` and `chezmoi`.
It utilizes `stow` and a config file to manage dotfiles of multiple programs on different systems.

## Installation

Requirements: `pip` & `stow`

`pip install stowd`

## Setup

Within the dotfiles directory, create a separate sub-directory for each program.
Within each sub-directory organize that programs config files as they appear from the home or root directory.

<details>
  <summary>Example dotfiles directory structure:</summary>

```
.
├── stowd
│   └── .config
│       └── stowd
│           └── stowd.cfg
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

Check the sample [stowd.cfg](sample/stowd.cfg) file for details.

## Usage

Run `stowd` without arguments to use all the settings from the config file.

<details>
  <summary>stowd -h</summary>

```
usage: stowd [-h] [-s DIR [DIR ...]] [-S DIR [DIR ...]] [-u DIR [DIR ...]]
                [-U DIR [DIR ...]] [-p NAME] [-c PATH] [-d PATH] [-v] [-r]
                [DIR ...]

Symlink dotfiles into their respective directories using `stow`.

positional arguments:
  DIR                   stow dir[s] to the home directory

options:
  -h, --help            show this help message and exit
  -s DIR [DIR ...], --stow DIR [DIR ...]
                        stow dir[s] to the home directory
  -S DIR [DIR ...], --stow-root DIR [DIR ...]
                        stow dir[s] to the root directory
  -u DIR [DIR ...], --unstow DIR [DIR ...]
                        unstow dir[s] from the home directory
  -U DIR [DIR ...], --unstow-root DIR [DIR ...]
                        unstow dir[s] from the root directory
  -p NAME, --platform NAME
                        platform(section) in config to use
  -c PATH, --config PATH
                        path to config file (stowd.cfg)
  -d PATH, --dotfiles PATH
                        path to dotfiles directory
  -v, --verbose         show verbose output
  -r, --root            allow stowing to root directory
```

</details>

## Examples

Here are my [dotfiles](https://github.com/ghassan0/dotfiles) to give you an idea of how your dotfiles directory would look like.
