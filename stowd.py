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


def is_boolean(string):
    """Check if a string represents a boolean"""

    bools = ["true", "false", "yes", "no", "on", "off", "1", "0"]
    return string.lower() in bools


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

    return platform


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


def get_settings(config, platform):
    """Return the settings from the config file"""

    if platform + "-settings" in config:
        settings = config["settings"]
    elif "settings" in config:
        settings = config["settings"]
    else:
        settings = []

    return settings


def get_setting(arg, settings, setting):
    """Return the setting [arg > config > default]"""

    if arg is not None:
        return arg[0]

    if setting == "dotfiles_dir":
        value = dir_path(settings.get(setting, "~/dotfiles"))
    elif setting == "quiet":
        value = settings.getboolean(setting, False)
    elif setting == "root":
        value = settings.getboolean(setting, True)
    else:
        value = None

    return value


def print_results(counter):
    """Print results."""

    print("Done.")
    if counter[0] > 0:
        print("Total stowd to '~': " + str(counter[0]))
    if counter[1] > 0:
        print("Total unstowd from '~': " + str(counter[1]))
    if counter[2] > 0:
        print("Total stowd to '/': " + str(counter[2]))
    if counter[3] > 0:
        print("Total unstowd from '/': " + str(counter[3]))
    if counter[4] > 0:
        print("Total ingnored: " + str(counter[4]))


def stow_from_args(args, dotfiles_dir, counter):
    """Stow from CLI args."""

    for app in args.stow:
        stow("~", dotfiles_dir, app, "stow")
        counter[0] += 1
    for app in args.unstow:
        stow("~", dotfiles_dir, app, "unstow")
        counter[1] += 1
    for app in args.stow_root:
        stow("/", dotfiles_dir, app, "stow")
        counter[2] += 1
    for app in args.unstow_root:
        stow("/", dotfiles_dir, app, "unstow")
        counter[3] += 1


def stow_from_config(config, platform, dotfiles_dir, counter):
    """Stow from config file."""

    platform_home = config[platform]
    for app in platform_home:
        if not is_boolean(platform_home.get(app)):
            print("[~] ingnored " + app)
            counter[4] += 1
        elif platform_home.getboolean(app):
            stow("~", dotfiles_dir, app, "stow")
            counter[0] += 1
        else:
            stow("~", dotfiles_dir, app, "unstow")
            counter[1] += 1
    if platform + "-root" in config:
        platform_root = config[platform + "-root"]
        for app in platform_root:
            if not is_boolean(platform_root.get(app)):
                print("[/] ingnored " + app)
                counter[4] += 1
            elif platform_root.getboolean(app):
                stow("/", dotfiles_dir, app, "stow")
                counter[2] += 1
            else:
                stow("/", dotfiles_dir, app, "unstow")
                counter[3] += 1


def main() -> None:
    """Stow/unstow dotfiles to home/root directories."""

    args = getargs()
    config = get_config(args.config_file, args.dotfiles_dir)
    platform = get_platform(config, args.platform)
    settings = get_settings(config, platform)

    dotfiles_dir = get_setting(args.dotfiles_dir, settings, "dotfiles_dir")

    counter = [0] * 5

    stow_from_args(args, dotfiles_dir, counter)

    if sum(counter) == 0 or args.platform is not None:
        stow_from_config(config, platform, dotfiles_dir, counter)

    print_results(counter)


if __name__ == "__main__":
    main()
