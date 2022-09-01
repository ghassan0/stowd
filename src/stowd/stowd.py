"""
Easily manage all your dotfiles across your devices.
"""

import sys
from importlib.metadata import version

from .options.args import getargs
from .options.config import get_config
from .options.settings import get_settings
from .stow.print_results import print_results
from .stow.stow import stow_from_args, stow_from_config
from .stow.stow_exists import stow_exists


def main() -> None:
    """Stow/unstow dotfiles to home/root directories."""
    # parse command line arguments
    args = getargs()

    # print app version and exit
    if args.version:
        print(version("stowd"))
        sys.exit(0)

    # check if stow exists
    stow_exists()

    # config file
    config = get_config(args.config_file, args.dotfiles_dir)

    # set setting from (command line arguments > config file > default)
    settings = get_settings(args, config["settings"])

    # print that we're in Simulation mode
    if settings["simulate"]:
        print("Simulation mode: no filesystem modifications")

    counter = [0] * 5

    # [un]stow[-root] from command line arguments
    stow_from_args(args, counter, settings)

    # [un]stow[-root] from config file
    if sum(counter) == 0 or args.platform is not None:
        stow_from_config(config["home"], config["root"], counter, settings)

    # print results
    if not settings["quiet"]:
        print_results(counter)


if __name__ == "__main__":
    main()
