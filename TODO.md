# To-do list

All planned notable changes to this project will be documented in this file.
Once a listing is completed, it will be moved to the Changelog.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [General]

### Fixed

- Remove requirement for config file if the --dotfiles_dir flag is used along with the add/remove subcommand
- Handle invalid config file (duplicate sections, etc.)

### Added

- Add ignore setting and flag to ignore files ending in this Perl regex.
- Add 'git clone' functionality to setup dotfiles repo on new device
- Return `platform` flag functionality and rename to `section`
- Add flag to disable inheriting from parent section (hostname - system - general)
- Consider adding Distro section (hostname - distro - system - general)

### Changed

- Maybe multiprocessing support for fun/learning
- Remove `stow` requirement and use python implementation (such as dploy)

### Removed

### Deprecated

### Security
