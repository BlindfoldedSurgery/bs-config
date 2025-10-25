# bs-config

[![CI status][github-actions-image]][github-actions-link]
[![codecov][codecov-image]][codecov-link]

[github-actions-image]: https://github.com/blindfoldedsurgery/bs-config/actions/workflows/workflow.yml/badge.svg
[github-actions-link]: https://github.com/blindfoldedsurgery/bs-config/actions/workflows/workflow.yml

[codecov-image]: https://codecov.io/gh/BlindfoldedSurgery/bs-config/graph/badge.svg?token=GXR5GIAQ20
[codecov-link]: https://codecov.io/gh/BlindfoldedSurgery/bs-config

## Usage

This package provides an `Env` class for easy access and validation of configuration values from
the environment or TOML files.

**Example**:

```python
from bs_config import Env

env = Env.load()

# a: int | None (missing or blank values lead to the default None)
a = env.get_int("my-int")

# b: int (you specified a default, so it can't be None)
b = env.get_int("my-iny", default=42)

# c: int (if the value is missing, a ValueError is raised)
c = env.get_int("my-int", required=True)
```

### Nested Values

You can access nested values by either separating keys with a dot, or using a scoped Env instance:

```python
from bs_config import Env

env = Env.load()
a = env.get_int("nested.my-int")

nested_env = env / "nested"
b = nested_env.get_int("my-int")

assert a == b
```

### Key Translation

For environment variables and Dotenv values, keys are translated to SCREAMING_SNAKE_CASE.
Nested scopes are translated to a **double** underscore, so the key `nested-section.my-value` becomes
`NESTED_SECTION__MY_VALUE`.

### Dotenv Support

If you install the package with the `dotenv` extra (`pip install bs-config[dotenv]`), you can load
the contents of `.env` files in addition to the environment variables from `os.environ`:

```python
from bs_config import Env

# Includes values from the .env file (if present)
env = Env.load(include_default_dotenv=True)

# Includes values from the test.env and dev.env files (if present)
env = Env.load(additional_dotenvs=["test", "dev"])
```

### TOML Support

You can also load TOML config files into an Env instance. Note that given paths are allowed to not
exist, and dotenv/env values take precedence.

```python
from bs_config import Env
from pathlib import Path

env = Env.load(toml_configs=[Path("/etc/myapp/config.toml")])
```
