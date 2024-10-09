# To-do list

All planned notable changes to this project will be documented in this file.
Once a listing is completed, it will be moved to the Changelog.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [General]

### Fixed

- Remove requirement for config file if the --dotfiles_dir flag is used along with the add/remove subcommand
- Handle invalid config file (other than duplicate sections)

### Added

- Add ignore setting and flag to ignore files ending in this Perl regex.
- Return `platform` flag functionality and rename to `section`

### Changed

- Maybe multiprocessing support for fun/learning
- Remove `stow` requirement and use python implementation (such as dploy)

### Removed

### Deprecated

### Security
