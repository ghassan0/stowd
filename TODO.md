# To-do list

All planned notable changes to this project will be documented in this file.
Once a listing is completed, it will be moved to the Changelog.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [General]

### Fixed

- Remove requirement for config file if the --dotfiles_dir flag is used along with the --[un]stow[-root] flag(s)

### Added

### Changed

- Divide codebase into sub-modules

### Removed

### Deprecated

### Security

## [Settings]

### Added

- Add root-only setting and flag to only run [un]stow-root
- Add dry-run setting and flag to only display what what happen if run normally
- Add ignore setting and flag to ignore files ending in this Perl regex.
