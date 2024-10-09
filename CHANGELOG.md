# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Handle invalid config file (duplicate sections)

### Added

- Look for `doti.cfg` in current directory or in `doti` folder within current directory
- Add an `ignore` and an `error` counter
- New Distro section (hostname - distro - system - general)

### Changed

- Default to enable root and substitute `root-enable` flag to `root-disable`
- Make each program add/remove operation atomic. Only allow changes to be made if no errors occur for that program 

### Deprecated

- Removed looking for `doti.cfg` in `XDA_CONFIG_HOME`

## [0.3.1] - 2022-09-11

### Fixed

- Removed debug message
- Fix naming of output
- Fix `--dotfiles` and `--config` argument inputs

## [0.3.0] - 2022-09-11

### Fixed

- Respect XDG paths for config

### Added

- Add setting to disable inheriting from parent section (hostname - system - general)
- Add freebsd, openbsd, and cygwin support.
- Add Arch Linux (AUR) install method.

### Changed

- Renamed program to `doti` from `stowd` (github/pypi/aur)
- Changed `[un]stow[-root]` flags into `add` and `remove` subcommands
- Config file path precedence order (argument > XDG > `~/.config` > based on `dotfiles-dir` arg > based on `~/dotfiles` > based on `~/.dotfiles`)
- Replaced 'stowd' and 'unstowd' boolean values to 'add' and 'remove'/'rm' in config

### Deprecated

- Removed `[un]stow[-root]` flags

## [0.2.1] - 2022-09-07

### Fixed

- Fix error when using arguments (was checking for a removed argument '--platform')
- Fix error handling when real file already exists at target location

## [0.2.0] - 2022-09-02

### Fixed

- Can run the same [un]stow[-root] flag multiple times

### Added

- Add platform specific settings
- Add hostname specific settings, home, and root sections
- Add root-only setting and flag to only run [un]stow-root using the 'root' sections in the config

### Changed

- Divide codebase into sub-modules
- Clean up sub-modules.
- Treat 'settings', 'home', 'root' sections as 'default' sections
- System specific home section is now '[SYSTEM]-home' instead of just '[SYSTEM]'
- Change 'root' flag and setting to 'root-enable'
- If app option is set to `false` and its directory doesn't exist, ignore instead of printing it out
- Add 'stowd' and 'stow' as true values and 'unstowd' and 'unstow' as false values in config

### Deprecated

- Removed 'platform' command-line argument for now

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

[unreleased]: https://github.com/alduraibi/stowd/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/alduraibi/stowd/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/alduraibi/stowd/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/alduraibi/stowd/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/alduraibi/stowd/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/alduraibi/stowd/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alduraibi/stowd/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/alduraibi/stowd/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/alduraibi/stowd/releases/tag/v0.0.1
