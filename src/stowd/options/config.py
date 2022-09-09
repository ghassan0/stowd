"""
Parse configuration file (stowd.cfg).
"""

import configparser
from os import environ
from os.path import expanduser, isfile

from ..helpers.system import get_hostname, get_system

CONFIG_FILE = "stowd.cfg"
DEFAULT_SECTION = "LEAVE_THIS_SECTION_EMPTY"


def get_config_file(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""
    default_config_path = ".config/stowd/" + CONFIG_FILE
    if args_config_file is not None:
        config_file = args_config_file[0]
    elif "XDG_CONFIG_HOME" in environ and isfile(
        expanduser(environ["XDG_CONFIG_HOME"] + "/stowd/" + CONFIG_FILE)
    ):
        config_file = expanduser(environ["XDG_CONFIG_HOME"] + "/stowd/" + CONFIG_FILE)
    elif isfile(expanduser("~/" + default_config_path)):
        config_file = expanduser("~/" + default_config_path)
    elif args_dotfiles_dir is not None:
        dotfiles_dir = args_dotfiles_dir[0]
        if isfile(dotfiles_dir + "/stowd/" + default_config_path):
            config_file = dotfiles_dir + "/stowd/" + default_config_path
    elif isfile(expanduser("~/dotfiles/stowd/" + default_config_path)):
        config_file = expanduser("~/dotfiles/stowd/" + default_config_path)
    elif isfile(expanduser("~/.dotfiles/stowd/" + default_config_path)):
        config_file = expanduser("~/.dotfiles/stowd/" + default_config_path)

    if "config_file" not in locals():
        raise FileNotFoundError(
            "Config file not found in `$XDG_CONFIG_HOME/stowd/"
            + CONFIG_FILE
            + "` or `~/.config/stowd/"
            + CONFIG_FILE
            + "`"
        )

    config = configparser.ConfigParser(default_section=DEFAULT_SECTION)
    config.read(config_file)

    return config


def get_section(config, section):
    """Returns specific section from config."""
    if section in config:
        return dict(config[section])
    return {}


def get_config_section(config, suffix):
    """Return the dict of section from the config file"""
    section_hostname = get_section(config, get_hostname() + "-" + suffix)
    section_system = get_section(config, get_system() + "-" + suffix)
    section_all = get_section(config, suffix)

    sections = section_all | section_system | section_hostname

    return sections


def get_config(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""
    config_file = get_config_file(args_config_file, args_dotfiles_dir)

    config = {}
    config["settings"] = get_config_section(config_file, "settings")
    config["home"] = get_config_section(config_file, "home")
    config["root"] = get_config_section(config_file, "root")
    return config
