"""
Perform the 'stow' command.
"""

import subprocess
from os.path import expanduser, isdir

from ..helpers.boolean import is_bool, is_true
from ..helpers.flatten_list import flatten_list


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
        if cmd == "stow":
            print(app + " directory not found in " + settings["dotfiles_dir"] + ".")
        counter[4] += 1
        if settings["verbose"]:
            print("[" + target_dir + "] ignored " + app)
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
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            print("ERROR: Failed to " + cmd + " " + app + "at [" + target_dir + "]")
            print("       A real file probably exists at target location.")
        else:
            if settings["verbose"]:
                print("[" + target_dir + "] " + cmd + "d " + app)
            stow_counter(target_dir, cmd, counter)


def stow_from_args(args, counter, settings):
    """Stow from CLI args."""
    if args.root:
        base_dir = "/"
    else:
        base_dir = "~"

    if args.subcmd == "add":
        for app in flatten_list(args.stow):
            stow(base_dir, "stow", app, counter, settings)
    else:
        for app in flatten_list(args.unstow):
            stow(base_dir, "unstow", app, counter, settings)


def stow_from_config(home, root, counter, settings):
    """Stow from config file."""
    if not settings["root-only"]:
        for app in home:
            if not is_bool(home.get(app)):
                if settings["verbose"]:
                    print("[~] ingnored " + app)
                counter[4] += 1
            elif is_true(home.get(app)):
                stow("~", "stow", app, counter, settings)
            else:
                stow("~", "unstow", app, counter, settings)
    if settings["root-only"] or settings["root-enable"]:
        for app in root:
            if not is_bool(root.get(app)):
                if settings["verbose"]:
                    print("[/] ingnored " + app)
                counter[4] += 1
            elif is_true(root.get(app)):
                stow("/", "stow", app, counter, settings)
            else:
                stow("/", "unstow", app, counter, settings)
