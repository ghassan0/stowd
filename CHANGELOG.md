# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2022-08-28

### Added

- Packaged into a PyPI package.
- Use stowd.cfg as config file.
- CLI flag to specify config file.
- CLI flag to specify platform to use from config file.
- CLI flag and config setting to specify dotfile directory.
- CLI flags to stow/unstow specified apps to home/root.
- CLI flag and config setting to enable using root directory.
- CLI flag and config setting to enable verbose output.
- Use stow to add/remove symlinks to dotfiles.
- New check to ensure stow is installed before running.
- Output the number of operations performed.
- New README file.
- New CHANGELOG file.
- GPLv3 License.
- Linux, Termux, and OSX support.
- New Github actions to auto package and release to Github and PyPI
- New Github action to update CHANGELOG after release

[unreleased]: https://github.com/ghassan0/stowd/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/ghassan0/stowd/releases/tag/v0.0.1
