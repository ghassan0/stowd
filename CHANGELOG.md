# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Can run the same [un]stow[-root] flag multiple times

## [0.1.0] - 2022-08-30

### Added

- Created TODO.md inspired by the 'Keep a Changelog' format
- Add quiet setting and flag to suppress regular output
- Add version flag to display current version number
- Add simulate setting and flag to display what happens if run normally with no filesystem modifications

## [0.0.2] - 2022-08-28

### Fixed

- Running the stowd command now works

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

[unreleased]: https://github.com/ghassan0/stowd/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ghassan0/stowd/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/ghassan0/stowd/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/ghassan0/stowd/releases/tag/v0.0.1
