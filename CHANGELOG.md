# Changelog

## v3.1.0 (2025-10-24)

### Feat

- implement getters for times, dates and datetimes

## v3.0.0 (2025-10-23)

### BREAKING CHANGE

- Env getters now expect a kebab-case key with scopes
separated by dots. For values loaded from the process environment or a
dotenv file, the keys will be translated to screaming snake case and
scopes will be separated by a **double** underscore (`__`).


- remove deprecated Env.scoped() method

## v2.0.0 (2025-10-23)

### BREAKING CHANGE

- Python 3.11 and 3.12 are no longer supported

### Feat

- introduce new scoping syntax
- add transform parameter for Env.get_string_list()
- add transform parameter for Env.get_string()


- bump minimum Python version to 3.13

## v1.2.0 (2025-10-11)

### Feat

- support Python 3.14

## v1.1.2 (2025-09-17)

### Fix

- avoid removing keys from dict during iteration

## v1.1.1 (2024-12-06)

### Fix

- Disable Python updates

## v1.1.0 (2024-10-18)

### Feat

- Support Python 3.13

## v1.0.2 (2024-06-22)

### Fix

- Ignore all cache folders

## v1.0.1 (2023-12-17)

### Fix

- **deps**: update pre-commit hook commitizen-tools/commitizen to v3

## 1.0.0

Same as 0.3.0.

## 0.3.0

### Features

- Allow scoping Env instances using `Env.scoped`

### Breaking Changes

- Replace Env constructor with `Env.load_from_dict` classmethod

## 0.2.0

### Breaking Changes

- Dropped Python 3.10 support

### New

- Support Python 3.12

## 0.1.1

Fix for Python 3.11 support.

## 0.1.0

Initial release.
