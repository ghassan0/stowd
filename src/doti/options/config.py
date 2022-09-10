"""
Parse configuration file (doti.cfg).
"""

import configparser
from os import environ
from os.path import expanduser, isfile

from ..helpers.boolean import is_true
from ..helpers.metadata import __config_file__, __project__
from ..helpers.system import get_hostname, get_system

DEFAULT_SECTION = "LEAVE_THIS_SECTION_EMPTY"


def get_config_file(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""
    config_subpath = "/" + __project__ + "/" + __config_file__
    default_config_path = ".config" + config_subpath
    dotfiles_config_path = __project__ + "/" + default_config_path

    if args_config_file is not None:
        config_file = args_config_file[0]
    elif "XDG_CONFIG_HOME" in environ and isfile(
        expanduser(environ["XDG_CONFIG_HOME"] + config_subpath)
    ):
        config_file = expanduser(environ["XDG_CONFIG_HOME"] + config_subpath)
    elif isfile(expanduser("~/" + default_config_path)):
        config_file = expanduser("~/" + default_config_path)
    elif args_dotfiles_dir is not None:
        dotfiles_dir = args_dotfiles_dir[0]
        if isfile(dotfiles_dir + "/" + dotfiles_config_path):
            config_file = dotfiles_dir + "/" + dotfiles_config_path
    elif isfile(expanduser("~/.dotfiles/" + dotfiles_config_path)):
        config_file = expanduser("~/.dotfiles/" + dotfiles_config_path)
    elif isfile(expanduser("~/dotfiles/" + dotfiles_config_path)):
        config_file = expanduser("~/dotfiles/" + dotfiles_config_path)

    if "config_file" not in locals():
        raise FileNotFoundError(
            "Config file not found in `$XDG_CONFIG_HOME"
            + config_subpath
            + "` or `~/"
            + default_config_path
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
    inherit_flag = "inherit"

    section_hostname = get_section(config, get_hostname() + "-" + suffix)
    settings_hostname = get_section(config, get_hostname() + "-settings")
    if inherit_flag in settings_hostname and (
        not is_true(settings_hostname[inherit_flag])
    ):
        return section_hostname

    section_system = get_section(config, get_system() + "-" + suffix)
    settings_system = get_section(config, get_system() + "-settings")
    if (inherit_flag in settings_system) and (
        not is_true(settings_system[inherit_flag])
    ):
        return section_system | section_hostname

    section_general = get_section(config, suffix)
    return section_general | section_system | section_hostname


def get_config(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""
    config_file = get_config_file(args_config_file, args_dotfiles_dir)

    config = {}
    config["settings"] = get_config_section(config_file, "settings")
    config["home"] = get_config_section(config_file, "home")
    config["root"] = get_config_section(config_file, "root")
    return config
