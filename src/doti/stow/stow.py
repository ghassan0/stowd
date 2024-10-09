"""
Perform the 'stow' command.
"""

import subprocess
from os.path import expanduser, isdir

from ..helpers.boolean import is_bool, is_true


def stow_counter(target_dir, cmd, counter):
    """Update counter for stow/unstow."""
    if target_dir == "~" and cmd == "add":
        counter[0] += 1
    elif target_dir == "~" and cmd == "remove":
        counter[1] += 1
    elif target_dir == "/" and cmd == "add":
        counter[2] += 1
    elif target_dir == "/" and cmd == "remove":
        counter[3] += 1
    elif cmd == "ignore":
        counter[4] += 1
    elif cmd == "error":
        counter[5] += 1


def stow(target_dir, cmd, app, counter, settings):
    """Runs the `stow` command."""
    if not isdir(expanduser(settings["dotfiles_dir"] + "/" + app)):
        if cmd == "add":
            print(app + " directory not found in " + settings["dotfiles_dir"] + ".")
        stow_counter(target_dir, "ignore", counter)
        if settings["verbose"]:
            print("Ignored " + app + "config files")
    else:
        if cmd == "add":
            flag = "restow"
            preposition = "to"
            cmd_past_tense = "Added"
        elif cmd == "remove":
            flag = "delete"
            preposition = "from"
            cmd_past_tense = "Removed"
        command = [
            "stow",
            "--simulate",
            "--no-folding",
            "--dir=" + expanduser(settings["dotfiles_dir"]),
            "--target=" + expanduser(target_dir),
            "--" + flag,
            app,
        ]
        if target_dir == "/":
            command.insert(0, "sudo")
            target_dir_name = "root"
        else: 
            target_dir_name = "home"
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("ERROR: Failed to " + cmd + " " + app + " config file(s) " + preposition + " the " + target_dir_name + " directory")
            print("       A real file[s] probably exists at target location.")
            stow_counter(target_dir, "error", counter)
        else:
            if not settings["simulate"]:
                command.remove("--simulate")
                try:
                    subprocess.run(
                        command,
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError:
                    print("ERROR: Unknown error using the 'stow' command]")
                    stow_counter(target_dir, "error", counter)
                else:
                    stow_counter(target_dir, cmd, counter)
            else:
                stow_counter(target_dir, cmd, counter)
            if settings["verbose"]:
                print(cmd_past_tense + " " + app + " config files " + preposition + " the " + target_dir_name + " directory")


def stow_from_args(args, counter, settings):
    """Stow from CLI args."""
    if args.root:
        base_dir = "/"
    else:
        base_dir = "~"

    if args.subcmd == "add":
        for app in args.stow:
            stow(base_dir, "add", app, counter, settings)
    else:
        for app in args.unstow:
            stow(base_dir, "remove", app, counter, settings)


def stow_from_config(home, root, counter, settings):
    """Stow from config file."""
    if not settings["root-only"]:
        for app in home:
            if not is_bool(home.get(app)):
                if settings["verbose"]:
                    print("Ignored " + app + "config files for the home directory")
                stow_counter("~", "ignore", counter)
            elif is_true(home.get(app)):
                stow("~", "add", app, counter, settings)
            else:
                stow("~", "remove", app, counter, settings)
    if settings["root-only"] or not settings["root-disable"]:
        for app in root:
            if not is_bool(root.get(app)):
                if settings["verbose"]:
                    print("Ignored " + app + "config files for the root directory")
                stow_counter("/", "ignore", counter)
            elif is_true(root.get(app)):
                stow("/", "add", app, counter, settings)
            else:
                stow("/", "remove", app, counter, settings)
