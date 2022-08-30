"""
Perform the 'stow' command.
"""

import subprocess
from os.path import expanduser, isdir

from ..helpers.flatten_list import flatten_list
from ..helpers.is_bool import is_bool


def stow_counter(target_dir, cmd, counter):
    """Update counter for stow/unstow."""
    if target_dir == "~" and cmd == "stow":
        counter[0] += 1
    elif target_dir == "~" and cmd == "unstow":
        counter[1] += 1
    elif target_dir == "/" and cmd == "stow":
        counter[2] += 1
    elif target_dir == "/" and cmd == "unstow":
        counter[3] += 1


def stow(target_dir, cmd, app, counter, settings):
    """Runs the `stow` command."""
    if not isdir(expanduser(settings["dotfiles_dir"] + "/" + app)):
        print(app + " directory not found in " + settings["dotfiles_dir"] + ".")
        counter[4] += 1
    else:
        if cmd == "stow":
            flag = "restow"
        elif cmd == "unstow":
            flag = "delete"
        command = [
            "stow",
            "--no-folding",
            "--dir=" + expanduser(settings["dotfiles_dir"]),
            "--target=" + expanduser(target_dir),
            "--" + flag,
            app,
        ]
        if settings["simulate"]:
            command.insert(1, "--simulate")
        if target_dir == "/":
            command.insert(0, "sudo")
        output = subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not output.returncode:
            if settings["verbose"]:
                print("[" + target_dir + "] " + cmd + "d " + app)
            stow_counter(target_dir, cmd, counter)
        else:
            print("ERROR: failed to " + cmd + " " + app + "at [" + target_dir + "]")


def stow_from_args(args, counter, settings):
    """Stow from CLI args."""
    for app in flatten_list(args.stow):
        stow("~", "stow", app, counter, settings)
    for app in flatten_list(args.unstow):
        stow("~", "unstow", app, counter, settings)
    for app in flatten_list(args.stow_root):
        stow("/", "stow", app, counter, settings)
    for app in flatten_list(args.unstow_root):
        stow("/", "unstow", app, counter, settings)


def stow_from_config(config, platform, counter, settings):
    """Stow from config file."""
    platform_home = config[platform]
    for app in platform_home:
        if not is_bool(platform_home.get(app)):
            if settings["verbose"]:
                print("[~] ingnored " + app)
            counter[4] += 1
        elif platform_home.getboolean(app):
            stow("~", "stow", app, counter, settings)
        else:
            stow("~", "unstow", app, counter, settings)
    if platform + "-root" in config and settings["root"]:
        platform_root = config[platform + "-root"]
        for app in platform_root:
            if not is_bool(platform_root.get(app)):
                if settings["verbose"]:
                    print("[/] ingnored " + app)
                counter[4] += 1
            elif platform_root.getboolean(app):
                stow("/", "stow", app, counter, settings)
            else:
                stow("/", "unstow", app, counter, settings)
