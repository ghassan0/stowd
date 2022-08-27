"""
Symlink dotfiles into their respective directories using `stow`.
"""

import argparse
import configparser
import subprocess
import sys
from os import environ
from os.path import expanduser, isdir, isfile
from shutil import which

CONFIG_FILE = "stowd.cfg"


def stow_exists():
    """Ensure `stow` exists."""
    if not which("stow"):
        Exception("Please install `stow` then try again.")


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


def is_bool(string):
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
        type=str,
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
        help="path to config file (" + CONFIG_FILE + ")",
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
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="show verbose output",
    )
    parser.add_argument(
        "-r",
        "--root",
        dest="root",
        action="store_true",
        help="allow stowing to root directory",
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
            if isfile(dotfiles_dir + "/stowd/.config/stowd/" + CONFIG_FILE):
                config_file = dotfiles_dir + "/stowd/.config/stowd/" + CONFIG_FILE
            elif isfile(dotfiles_dir + "/stowd/." + CONFIG_FILE):
                config_file = dotfiles_dir + "/stowd/." + CONFIG_FILE
        if isfile(expanduser("~/.config/stowd/" + CONFIG_FILE)):
            config_file = expanduser("~/.config/stowd/" + CONFIG_FILE)
        elif isfile(expanduser("~/." + CONFIG_FILE)):
            config_file = expanduser("~/." + CONFIG_FILE)
        elif isfile(expanduser("~/dotfiles/stowd/.config/stowd/" + CONFIG_FILE)):
            config_file = expanduser("~/dotfiles/stowd/.config/stowd/" + CONFIG_FILE)
        elif isfile(expanduser("~/dotfiles/stowd/." + CONFIG_FILE)):
            config_file = expanduser("~/dotfiles/stowd/." + CONFIG_FILE)
        elif isfile(expanduser("~/.dotfiles/stowd/.config/stowd/" + CONFIG_FILE)):
            config_file = expanduser("~/.dotfiles/stowd/.config/stowd/" + CONFIG_FILE)
        elif isfile(expanduser("~/.dotfiles/stowd/." + CONFIG_FILE)):
            config_file = expanduser("~/.dotfiles/stowd/." + CONFIG_FILE)

    if "config_file" not in locals() or not isfile(config_file):
        raise FileNotFoundError(
            "Config file not found in `~/.config/stowd/"
            + CONFIG_FILE
            + "` or `~/."
            + CONFIG_FILE
            + "`"
        )

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
        Exception(platform + " section missing in config file")

    return platform


def get_config_settings(config, platform):
    """Return the settings from the config file"""
    if platform + "-settings" in config:
        settings = config["settings"]
    elif "settings" in config:
        settings = config["settings"]
    else:
        settings = []

    return settings


def get_setting(arg, config_settings, setting):
    """Return the setting [arg > config > default]"""
    if setting == "dotfiles_dir":
        if arg is not None:
            return arg
        value = dir_path(config_settings.get(setting, "~/dotfiles"))
    elif setting in ["verbose", "root"]:
        if arg:
            return arg
        value = config_settings.getboolean(setting, False)
    else:
        value = None

    return value


def get_settings(args, config_settings):
    """Return all settings."""
    settings = {}
    settings["dotfiles_dir"] = get_setting(
        args.dotfiles_dir, config_settings, "dotfiles_dir"
    )
    settings["verbose"] = get_setting(args.verbose, config_settings, "verbose")
    settings["root"] = get_setting(args.root, config_settings, "root")

    return settings


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
        if target_dir == "/":
            command.insert(0, "sudo")
        output = subprocess.run(
            command,
            check=True,
        )
        if not output.returncode:
            if settings["verbose"]:
                print("[" + target_dir + "] " + cmd + "d " + app)
            stow_counter(target_dir, cmd, counter)


def stow_from_args(args, counter, settings):
    """Stow from CLI args."""
    for app in args.stow:
        stow("~", "stow", app, counter, settings)
    for app in args.unstow:
        stow("~", "unstow", app, counter, settings)
    for app in args.stow_root:
        stow("/", "stow", app, counter, settings)
    for app in args.unstow_root:
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


def print_results(counter):
    """Print results."""
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
    if sum(counter) == 0:
        print("Nothing done")


def main() -> None:
    """Stow/unstow dotfiles to home/root directories."""
    stow_exists()
    args = getargs()
    config = get_config(args.config_file, args.dotfiles_dir)
    platform = get_platform(config, args.platform)
    config_settings = get_config_settings(config, platform)

    settings = get_settings(args, config_settings)

    counter = [0] * 5

    stow_from_args(args, counter, settings)

    if sum(counter) == 0 or args.platform is not None:
        stow_from_config(config, platform, counter, settings)

    print_results(counter)


if __name__ == "__main__":
    main()
