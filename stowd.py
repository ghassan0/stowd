"""
Symlink dotfiles into their respective directories using `stow`.
"""

import argparse
import configparser
import subprocess
import sys
from os import environ
from os.path import expanduser, isdir, isfile


def dir_path(string):
    """Ensure directory exists."""
    if isdir(expanduser(string)):
        return expanduser(string)
    raise NotADirectoryError(string)


def file_path(string):
    """Ensure file exists."""
    if isfile(expanduser(string)):
        return expanduser(string)
    raise FileNotFoundError(string)


def getargs():
    """Parses and returns CLI arguments."""

    parser = argparse.ArgumentParser(
        description="Symlink dotfiles into their respective directories using \
                `stow`."
    )
    parser.add_argument(
        dest="stow",
        nargs="*",
        default=[],
        metavar="DIR",
        help="stow dir[s] to the home directory",
    )
    parser.add_argument(
        "-s",
        "--stow",
        dest="stow",
        nargs="+",
        default=[],
        metavar="DIR",
        help="stow dir[s] to the home directory",
    )
    parser.add_argument(
        "-S",
        "--stow-root",
        dest="stow_root",
        nargs="+",
        default=[],
        metavar="DIR",
        help="stow dir[s] to the root directory",
    )
    parser.add_argument(
        "-u",
        "--unstow",
        dest="unstow",
        nargs="+",
        default=[],
        metavar="DIR",
        help="unstow dir[s] from the home directory",
    )
    parser.add_argument(
        "-U",
        "--unstow-root",
        dest="unstow_root",
        nargs="+",
        default=[],
        metavar="DIR",
        help="unstow dir[s] from the root directory",
    )
    parser.add_argument(
        "-p",
        "--platform",
        dest="platform",
        nargs=1,
        metavar="NAME",
        help="platform(section) in config to use",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        nargs=1,
        type=file_path,
        metavar="PATH",
        help="path to config file (stowd.ini)",
    )
    parser.add_argument(
        "-d",
        "--dotfiles",
        dest="dotfiles_dir",
        nargs=1,
        type=dir_path,
        metavar="PATH",
        help="path to dotfiles directory",
    )

    args = parser.parse_args()
    return args


def get_config(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""

    if args_config_file is not None:
        config_file = args_config_file[0]
    else:
        if args_dotfiles_dir is not None:
            dotfiles_dir = args_dotfiles_dir[0]
            if isfile(dotfiles_dir + "/stowd/.config/stowd/stowd.ini"):
                config_file = dotfiles_dir + "/stowd/.config/stowd/stowd.ini"
            elif isfile(dotfiles_dir + "/stowd/.stowd.ini"):
                config_file = dotfiles_dir + "/stowd/.stowd.ini"
        if isfile(expanduser("~/.config/stowd/stowd.ini")):
            config_file = expanduser("~/.config/stowd/stowd.ini")
        elif isfile(expanduser("~/.stowd.ini")):
            config_file = expanduser("~/.stowd.ini")
        elif isfile(expanduser("~/dotfiles/stowd/.config/stowd/stowd.ini")):
            config_file = expanduser("~/dotfiles/stowd/.config/stowd/stowd.ini")
        elif isfile(expanduser("~/dotfiles/stowd/.stowd.ini")):
            config_file = expanduser("~/dotfiles/stowd/.stowd.ini")
        elif isfile(expanduser("~/.dotfiles/stowd/.config/stowd/stowd.ini")):
            config_file = expanduser("~/.dotfiles/stowd/.config/stowd/stowd.ini")
        elif isfile(expanduser("~/.dotfiles/stowd/.stowd.ini")):
            config_file = expanduser("~/.dotfiles/stowd/.stowd.ini")

    if "config_file" not in locals() or not isfile(config_file):
        print("Config file not found in `~/.config/stowd/stowd.ini` or `~/.stowd.ini`")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def get_dotfiles_dir(args_dotfiles_dir, settings):
    """Returns the dotfiles directory."""

    if args_dotfiles_dir is not None:
        dotfiles_dir = args_dotfiles_dir[0]
    else:
        if "dotfiles_dir" in settings:
            dotfiles_dir = dir_path(settings["dotfiles_dir"])
        elif isdir(expanduser("~/dotfiles")):
            dotfiles_dir = expanduser("~/dotfiles")
        elif isdir(expanduser("~/.dotfiles")):
            dotfiles_dir = expanduser("~/.dotfiles")
        else:
            print("No dotfiles directory found.")
            sys.exit(1)

    return dotfiles_dir


def get_platform(config, args_platform):
    """Returns specific platform(section) from config."""

    if args_platform is not None:
        platform = args_platform[0]
    else:
        if "TERMUX_VERSION" in environ:
            platform = "termux"
        elif sys.platform == "darwin":
            platform = "osx"
        elif sys.platform == "win32":
            platform = "windows"
        else:
            platform = "linux"

    if platform not in config:
        print(platform + " section missing in config file")
        sys.exit(1)

    return config[platform]


def stow(target_dir, dotfiles_dir, app, cmd):
    """Runs the `stow` command."""

    app_path = dotfiles_dir + "/" + app
    if not isdir(expanduser(app_path)):
        print(app_path + " directory not found.")
    else:
        if cmd == "stow":
            flag = "restow"
        elif cmd == "unstow":
            flag = "delete"
        command = [
            "stow",
            "--no-folding",
            "--dir=" + expanduser(dotfiles_dir),
            "--target=" + expanduser(target_dir),
            "--" + flag,
            app,
        ]
        if target_dir == "/":
            command.insert(0, "sudo")
        output = subprocess.run(
            command,
            check=True,
        )
        if not output.returncode:
            print("[" + target_dir + "] " + cmd + "d " + app)


def main() -> None:
    """Stow/unstow dotfiles to home/root directories."""

    args = getargs()
    config = get_config(args.config_file, args.dotfiles_dir)

    if "settings" in config:
        settings = config["settings"]
    else:
        settings = []
    dotfiles_dir = get_dotfiles_dir(args.dotfiles_dir, settings)

    for app in args.stow:
        stow("~", dotfiles_dir, app, "stow")
    for app in args.unstow:
        stow("~", dotfiles_dir, app, "unstow")
    for app in args.stow_root:
        stow("/", dotfiles_dir, app, "stow")
    for app in args.unstow_root:
        stow("/", dotfiles_dir, app, "unstow")

    if len(sys.argv) == 1 or args.platform is not None:
        platform = get_platform(config, args.platform)
        for app in platform:
            if platform[app] == "stow":
                stow("~", dotfiles_dir, app, "stow")
            elif platform[app] == "unstow":
                stow("~", dotfiles_dir, app, "unstow")
            elif platform[app] == "stow-root":
                stow("/", dotfiles_dir, app, "stow")
            elif platform[app] == "unstow-root":
                stow("/", dotfiles_dir, app, "unstow")


if __name__ == "__main__":
    main()
