# Change Log

## 0.1.1

### Fixed

- Fix deploying to PyPI.

## 0.1.0

### Added

- Add support for Django 1.10 (#49).

### Changed

- Remove support for Django < 1.8, including South. (#49).

## 0.0.20

### Fixed

- Require a recent version of future (#45).

## 0.0.19

### Added

- Better error messages in mail steps (#42).

## 0.0.18

### Added

- Support passing a relative URL to `django_url` (#40).

## 0.0.17

### Fixed

- Normalize model name case when it's used in the features (#31).

## 0.0.16

### Fixed

- Fix model name case when it's used in the features (#30).

## 0.0.15

### Added

- Use South if it is installed (#28).

## 0.0.14

### Added

- Support for Django 1.9 (#24).
- Support for Django 1.3 (#22).

## 0.0.13

### Added

- Use `StaticLiveServerTestCase` when available (#18).

## 0.0.12

### Added

- `django_url` from Lettuce (#17).

## 0.0.11

### Fixed

- Working with many-to-many fields (#15).

## 0.0.10

### Fixed

- Passing attributes to `harvest` (#14).

## 0.0.9

### Added

- More email steps (#12).

## 0.0.8

### Added

- Steps for testing HTML alternatives in sent email (#11).

## 0.0.7

### Added

- Support for Django 1.4, 1.5 and 1.6 (#9).

## 0.0.6

### Changed

- Remove `hashes_data` (#7).
- Require explicit `None` for field name in `write_models` (#8).

## 0.0.5

### Changed

- Remove undocumented API for model steps (#4).

## 0.0.4

### Changed

- Always pass a list of hashes to `creates_models` and `writes_models`.

## 0.0.3

### Fixed

- Fix getting options from `GherkinPlugin`.

## 0.0.2

### Fixed

- Fix installing package from PyPI.

## 0.0.1

Initial PyPI release as Aloe-Django.
