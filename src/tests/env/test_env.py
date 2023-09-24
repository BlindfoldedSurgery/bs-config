import pytest
from _pytest.fixtures import fixture

from bs_config.env import Env


@fixture
def env() -> Env:
    return Env(
        {
            "string": "abc",
            "int": "42",
            "empty": "",
            "blank": "  ",
        }
    )


def test_get_string_value(env):
    value = env.get_string("string")
    assert value == "abc"


@pytest.mark.parametrize(
    "key",
    ["empty", "blank"],
)
@pytest.mark.parametrize("default", ["test", None])
def test_get_blank_string_default(env, key, default):
    value = env.get_string(key, default=default)
    assert value == default


@pytest.mark.parametrize(
    "key",
    ["empty", "blank", "MISSING KEY"],
)
def test_get_string_missing_no_default_required(env, key):
    with pytest.raises(ValueError, match=key):
        env.get_string(key, default=None, required=True)


@pytest.mark.parametrize(
    "default",
    [
        None,
        "test",
    ],
)
def test_get_string_value_default(env, default):
    value = env.get_string("missing", default=default)
    assert value == default


def test_get_string_value_required_with_default(env):
    value = env.get_string("missing", default="test", required=True)
    assert value == "test"


@pytest.mark.parametrize(
    "key,expected",
    [
        ("True", True),
        ("true", True),
        ("yes", True),
        ("no", False),
        ("false", False),
        ("unrelated", False),
    ],
)
def test_get_bool_value(key, expected):
    env = Env({key: key})
    value = env.get_bool(key, default=not expected)
    assert value == expected, f"Value '{key}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_empty_bool_value(value):
    env = Env({"KEY": value})
    value = env.get_bool("KEY", default=True)
    assert value is True, f"Value '{value}' does not trigger default value"


def test_get_int_value(env):
    value = env.get_int("int")
    assert value == 42


def test_get_invalid_int(env):
    with pytest.raises(ValueError):
        env.get_int("string")


@pytest.mark.parametrize(
    "default",
    [
        None,
        21,
    ],
)
def test_get_int_value_default(env, default):
    value = env.get_int("missing", default=default)
    assert value == default


def test_get_int_value_required_with_default(env):
    value = env.get_int("missing", default=21, required=True)
    assert value == 21


def test_get_int_value_required_no_default(env):
    with pytest.raises(ValueError, match="MISSING_KEY"):
        env.get_int("MISSING_KEY", default=None, required=True)
