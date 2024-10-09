"""
Parse doti configuration file (doti.cfg).
"""

import configparser
from os import environ
from os.path import expanduser, isfile

from ..helpers.boolean import is_true
from ..helpers.metadata import __config_file__, __project__
from ..helpers.system import get_hostname, get_distro, get_platform

DEFAULT_SECTION = "LEAVE_THIS_SECTION_EMPTY"


def get_config_file(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""

    if args_config_file is not None:
        if isfile(args_config_file[0]):
            config_file = args_config_file[0]
    elif isfile("./" + __config_file__):
        config_file = "./" + __config_file__
    elif isfile("./" + __project__ + "/" + __config_file__):
        config_file = "./" + __project__ + "/" + __config_file__

    try:
        if "config_file" not in locals():
            raise FileNotFoundError()
    except FileNotFoundError:
        print("Error: doti config file not found")
        exit(1)

    config = configparser.ConfigParser(default_section=DEFAULT_SECTION)

    try:
        config.read(config_file)
    except configparser.DuplicateSectionError:
        print("Error: Avoid duplicate sections in \"" + config_file + "\"")
        exit(1)

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

    section_distro = get_section(config, get_distro() + "-" + suffix)
    settings_distro = get_section(config, get_distro() + "-settings")
    if inherit_flag in settings_distro and (
        not is_true(settings_distro[inherit_flag])
    ):
        return section_distro | section_hostname

    section_platform = get_section(config, get_platform() + "-" + suffix)
    settings_platform = get_section(config, get_platform() + "-settings")
    if (inherit_flag in settings_platform) and (
        not is_true(settings_platform[inherit_flag])
    ):
        return section_platform | section_distro | section_hostname

    section_general = get_section(config, suffix)
    return section_general | section_platform | section_distro | section_hostname


def get_config(args_config_file, args_dotfiles_dir):
    """Reads and returns config from file."""
    config_file = get_config_file(args_config_file, args_dotfiles_dir)

    config = {}
    config["settings"] = get_config_section(config_file, "settings")
    config["home"] = get_config_section(config_file, "home")
    config["root"] = get_config_section(config_file, "root")
    return config
