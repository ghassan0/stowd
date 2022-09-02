"""
Return all settings (command-line argument > config file > default)
"""

from ..helpers.boolean import is_true
from ..helpers.path import dir_path


def get_setting(arg, config_settings, setting):
    """Return the setting (command-line argument > config file > default)"""
    if setting == "dotfiles_dir":
        if arg is not None:
            return arg
        return dir_path(config_settings.get(setting, "~/dotfiles"))
    if setting in ["verbose", "quiet", "root-enable", "root-only", "simulate"]:
        if arg:
            return arg
        return is_true(config_settings.get(setting, "false"))
    return arg


def get_settings(args, config_settings):
    """Return all settings."""
    settings = {}
    settings["dotfiles_dir"] = get_setting(
        args.dotfiles_dir, config_settings, "dotfiles_dir"
    )
    settings["verbose"] = get_setting(args.verbose, config_settings, "verbose")
    settings["quiet"] = get_setting(args.quiet, config_settings, "quiet")
    settings["root-enable"] = get_setting(
        args.root_enable, config_settings, "root-enable"
    )
    settings["root-only"] = get_setting(args.root_only, config_settings, "root-only")
    settings["simulate"] = get_setting(args.simulate, config_settings, "simulate")
    return settings
