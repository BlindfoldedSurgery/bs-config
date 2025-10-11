# bs-config

[![CI status][github-actions-image]][github-actions-link]
[![codecov][codecov-image]][codecov-link]

[github-actions-image]: https://github.com/blindfoldedsurgery/bs-config/actions/workflows/workflow.yml/badge.svg
[github-actions-link]: https://github.com/blindfoldedsurgery/bs-config/actions/workflows/workflow.yml

[codecov-image]: https://codecov.io/gh/BlindfoldedSurgery/bs-config/graph/badge.svg?token=GXR5GIAQ20
[codecov-link]: https://codecov.io/gh/BlindfoldedSurgery/bs-config
## Usage

For now, this package provides the `Env` class for easy access and validation of configuration
values from the environment. At its essence, it's just a wrapper around a `dict[str, str]` with
some fancy wrappers and fancy typing.

**Example**:

```python
from bs_config import Env

env = Env.load()

# a: int | None (missing or blank values lead to the default None)
a = env.get_int("MY_INT")

# b: int (you specified a default, so it can't be None)
b = env.get_int("MY_INT", default=42)

# c: int (if the value is missing, a ValueError is raised)
c = env.get_int("MY_INT", required=True)
```

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

## Future Plans

A higher-level extension is planned. It will allow users to just define a typed Python class
representing their config, which can then be automatically loaded.
