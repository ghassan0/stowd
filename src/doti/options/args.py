"""
Parse command-line arguments.
"""

import argparse

from ..helpers.metadata import __config_file__, __version__
from ..helpers.path import dir_path, file_path


def getargs():
    """Parses and returns CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Symlink dotfiles into their respective directories using `stow`."
    )
    # parser.add_argument(
    #     dest="stow",
    #     nargs="*",
    #     action="append",
    #     default=[],
    #     metavar="NAME",
    #     help="stow dir[s] to the home directory",
    # )
    parser.add_argument(
        "-r",
        "--root-enable",
        dest="root_enable",
        action="store_true",
        help="enable root section in config",
    )
    parser.add_argument(
        "-R",
        "--root-only",
        dest="root_only",
        action="store_true",
        help="only use root section in config",
    )
    # parser.add_argument(
    #     "-p",
    #     "--platform",
    #     dest="platform",
    #     nargs=1,
    #     type=str,
    #     metavar="PLATFORM",
    #     help="platform(section) in config to use",
    # )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        nargs=1,
        type=file_path,
        metavar="FILE",
        help="path to config file (" + __config_file__ + ")",
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
        action="version",
        version="%(prog)s v" + __version__,
        help="show version number",
    )

    sub_parsers = parser.add_subparsers(dest="subcmd")

    stow_sub_parser = sub_parsers.add_parser("add")
    stow_sub_parser.add_argument(
        dest="stow",
        nargs="+",
        metavar="NAME",
        help="stow dir[s] to the home directory",
    )
    stow_sub_parser.add_argument(
        "-r",
        "--root",
        dest="root",
        action="store_true",
        help="use root dir instead of home",
    )

    unstow_sub_parser = sub_parsers.add_parser("remove")
    unstow_sub_parser.add_argument(
        dest="unstow",
        nargs="+",
        metavar="NAME",
        help="unstow dir[s] from the home directory",
    )
    unstow_sub_parser.add_argument(
        "-r",
        "--root",
        dest="root",
        action="store_true",
        help="use root dir instead of home",
    )

    args = parser.parse_args()
    print(args)
    return args
