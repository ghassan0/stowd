"""
Parse command-line arguments.
"""

import argparse

from ..helpers.path import dir_path, file_path

CONFIG_FILE = "stowd.cfg"


def getargs():
    """Parses and returns CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Symlink dotfiles into their respective directories using `stow`."
    )
    parser.add_argument(
        dest="stow",
        nargs="*",
        action="append",
        default=[],
        metavar="NAME",
        help="stow dir[s] to the home directory",
    )
    parser.add_argument(
        "-s",
        "--stow",
        dest="stow",
        nargs="+",
        action="append",
        default=[],
        metavar="NAME",
        help="stow dir[s] to the home directory",
    )
    parser.add_argument(
        "-S",
        "--stow-root",
        dest="stow_root",
        nargs="+",
        action="append",
        default=[],
        metavar="NAME",
        help="stow dir[s] to the root directory",
    )
    parser.add_argument(
        "-u",
        "--unstow",
        dest="unstow",
        nargs="+",
        action="append",
        default=[],
        metavar="NAME",
        help="unstow dir[s] from the home directory",
    )
    parser.add_argument(
        "-U",
        "--unstow-root",
        dest="unstow_root",
        nargs="+",
        action="append",
        default=[],
        metavar="NAME",
        help="unstow dir[s] from the root directory",
    )
    parser.add_argument(
        "-r",
        "--root",
        dest="root",
        action="store_true",
        help="allow stowing to root directory",
    )
    parser.add_argument(
        "-p",
        "--platform",
        dest="platform",
        nargs=1,
        type=str,
        metavar="PLATFORM",
        help="platform(section) in config to use",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        nargs=1,
        type=file_path,
        metavar="FILE",
        help="path to config file (" + CONFIG_FILE + ")",
    )
    parser.add_argument(
        "-d",
        "--dotfiles",
        dest="dotfiles_dir",
        nargs=1,
        type=dir_path,
        metavar="DIR",
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
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="supress output",
    )
    parser.add_argument(
        "-n",
        "--no",
        "--simulate",
        dest="simulate",
        action="store_true",
        help="simulate run, no filesystem modification",
    )
    parser.add_argument(
        "-V",
        "--version",
        dest="version",
        action="store_true",
        help="show version number",
    )

    args = parser.parse_args()
    return args
