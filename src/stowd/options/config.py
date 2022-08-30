"""
Parse configuration file (stowd.cfg).
"""

import configparser
import sys
from os import environ
from os.path import expanduser, isfile

CONFIG_FILE = "stowd.cfg"


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


def get_platform(args_platform, config):
    """Returns specific platform(section) from config."""
    if args_platform is not None:
        platform = args_platform[0]
    else:
        if "TERMUX_VERSION" in environ:
            platform = "termux"
        elif sys.platform == "darwin":
            platform = "osx"
        # elif sys.platform == "win32":
        #     platform = "windows"
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
