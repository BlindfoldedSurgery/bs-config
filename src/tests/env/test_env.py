import pytest
from _pytest.fixtures import fixture

from bs_config.env import Env


@fixture
def env() -> Env:
    return Env(
        {
            "string": "abc",
            "string_trailing": " abc ",
            "int": "42",
            "int_trailing": " 42 ",
            "empty": "",
            "blank": "  ",
        }
    )


@pytest.mark.parametrize(
    "key",
    ["string", "string_trailing"],
)
def test_get_string_value(env, key):
    value = env.get_string(key)
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
        ("true ", True),
        (" true ", True),
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


@pytest.mark.parametrize(
    "key",
    ["int", "int_trailing"],
)
def test_get_int_value(env, key):
    value = env.get_int(key)
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


@pytest.mark.parametrize(
    "value,expected",
    [
        (",", []),
        (" ,", []),
        (", ", []),
        ("test", ["test"]),
        ("a,bc,d", ["a", "bc", "d"]),
        (",a,bc,,d,", ["a", "bc", "d"]),
        (" a , bc , d ", ["a", "bc", "d"]),
        ("a,hello world,b", ["a", "hello world", "b"]),
        ("1,2,34", ["1", "2", "34"]),
    ],
)
def test_get_string_list(value, expected):
    key = "KEY"
    env = Env({key: value})
    result = env.get_string_list(key)

    assert result == expected, f"'{value}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_string_list_blank(value):
    key = "KEY"
    env = Env({key: value})
    result = env.get_string_list(key)
    assert result is None


def test_get_string_list_missing_required():
    key = "KEY"
    env = Env({})
    with pytest.raises(ValueError, match=key):
        env.get_string_list(key, required=True)


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_string_list_blank_required(value):
    key = "KEY"
    env = Env({key: value})
    with pytest.raises(ValueError, match=key):
        env.get_string_list(key, required=True)


@pytest.mark.parametrize(
    "required",
    [True, False],
)
def test_get_string_list_default(env, required):
    value = env.get_string_list("missing", default=["test"], required=required)
    assert value == ["test"]


@pytest.mark.parametrize(
    "value,expected",
    [
        (",", []),
        (" ,", []),
        (", ", []),
        ("1234", [1234]),
        ("1,23,4", [1, 23, 4]),
        (",1,23,,4,", [1, 23, 4]),
        (" 1 , 23 , 4 ", [1, 23, 4]),
    ],
)
def test_get_int_list(value, expected):
    key = "KEY"
    env = Env({key: value})
    result = env.get_int_list(key)

    assert result == expected, f"'{value}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_int_list_blank(value):
    key = "KEY"
    env = Env({key: value})
    result = env.get_int_list(key)
    assert result is None


def test_get_int_list_missing_required():
    key = "KEY"
    env = Env({})
    with pytest.raises(ValueError, match=key):
        env.get_int_list(key, required=True)


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_int_list_blank_required(value):
    key = "KEY"
    env = Env({key: value})
    with pytest.raises(ValueError, match=key):
        env.get_int_list(key, required=True)


@pytest.mark.parametrize(
    "required",
    [True, False],
)
def test_get_int_list_default(env, required):
    value = env.get_int_list("missing", default=[42], required=required)
    assert value == [42]


@pytest.mark.parametrize(
    "value",
    [
        "a",
        " test ",
        "1,b,3",
        ",a,",
        "1 2",
    ],
)
def test_get_int_list_invalid_value(value):
    key = "KEY"
    env = Env({key: value})
    with pytest.raises(ValueError, match=key):
        env.get_int_list(key)
