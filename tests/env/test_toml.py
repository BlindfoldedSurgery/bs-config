from datetime import date, datetime, time
from pathlib import Path

import pytest

from bs_config import Env


@pytest.fixture
def example_env(example_file_loader) -> Env:
    return Env.load(toml_configs=[example_file_loader("example.toml")])


def file_does_not_exist():
    env = Env.load(toml_configs=[Path("missing.toml")])
    assert env is not None


def test_top_level_val(example_env):
    value = example_env.get_string("does-this")
    assert value == "work"


def test_simple_vals__string(example_env):
    value = example_env.get_string("top.string")
    assert value == "foo"


def test_simple_vals__bool(example_env):
    value = example_env.get_bool("top.bool", default=False)
    assert isinstance(value, bool)
    assert value


def test_simple_vals__int(example_env):
    value = example_env.get_int("top.int")
    assert value == 123


def test_simple_vals__int_default(example_env):
    value = example_env.get_int("missing", default=12)
    assert value == 12


def test_simple_vals__date(example_env):
    value = example_env.get_date("top.date")
    assert isinstance(value, date)
    assert value == date(1979, 5, 27)


def test_simple_vals__time(example_env):
    value = example_env.get_time("top.time")
    assert isinstance(value, time)
    assert value.tzinfo is None
    assert value == time(6, 32)


@pytest.mark.parametrize(
    "key,is_naive",
    [
        ("top.datetime-naive", True),
        ("top.datetime-aware", False),
        ("top.datetime-offset", False),
    ],
)
def test_simple_vals__datetime(example_env, key, is_naive):
    value = example_env.get_datetime(key, is_naive=is_naive)
    assert isinstance(value, datetime)
    assert (value.tzinfo is None) == is_naive


@pytest.mark.parametrize(
    "key,is_naive",
    [
        ("top.datetime-naive", True),
        ("top.datetime-aware", False),
        ("top.datetime-offset", False),
    ],
)
def test_simple_vals__datetime_mismatch(example_env, key, is_naive):
    with pytest.raises(ValueError):
        example_env.get_datetime(key, is_naive=not is_naive)


def test_float__int(example_env):
    with pytest.raises(ValueError):
        example_env.get_int("top.float")


def test_float__str(example_env):
    value = example_env.get_string("top.float")
    assert value == "13.4"


def test_float__transformed(example_env):
    value = example_env.get_string("top.float", transform=float)
    assert isinstance(value, float)
    assert value == 13.4


def test_nested_val__direct(example_env):
    value = example_env.get_string("top.nested.foo")
    assert isinstance(value, str)
    assert value == "nested"


def test_nested_val__scoped(example_env):
    scoped = example_env / "top" / "nested"
    value = scoped.get_string("foo")
    assert isinstance(value, str)
    assert value == "nested"


def test_list_strings(example_env):
    value = example_env.get_string_list("top.list-strings")
    assert isinstance(value, list)
    assert value == ["foo", "bar"]


def test_list_strings_nested(example_env):
    with pytest.raises(ValueError):
        example_env.get_string_list("top.list-nested")


def test_list_strings_empty(example_env):
    value = example_env.get_string_list("top.list-empty")
    assert value == []


def test_list_ints(example_env):
    value = example_env.get_int_list("top.list-ints")
    assert isinstance(value, list)
    assert value == [1, 2, 3]


def test_list_int_empty(example_env):
    value = example_env.get_int_list("top.list-empty")
    assert value == []


def test_list_ints_nested(example_env):
    with pytest.raises(ValueError):
        example_env.get_int_list("top.list-nested")


def test_list_floats(example_env):
    value = example_env.get_string_list("top.list-floats", transform=float)
    assert isinstance(value, list)
    assert value == [1.1, 1.2, 1.3]


def test_list_bools__as_string(example_env):
    with pytest.raises(ValueError):
        example_env.get_string_list("top.list-bools")


def test_list_bools__as_int(example_env):
    with pytest.raises(ValueError):
        example_env.get_int_list("top.list-bools")


def test_dict(example_env):
    value = example_env.get_string("top.dict.key")
    assert isinstance(value, str)
    assert value == "value"


@pytest.mark.parametrize(
    "key",
    ["missing", "top.missing"],
)
def test_unknown_key(example_env, key):
    value = example_env.get_string(key)
    assert value is None


def test_lookup_mistyped(example_env):
    with pytest.raises(ValueError):
        example_env.get_string("top.list-strings.invalid")


def test_list_of_dicts(example_env):
    with pytest.raises(ValueError):
        example_env.get_string_list("items")


def test_string_default(example_env):
    value = example_env.get_string("missing", default="value")
    assert isinstance(value, str)
    assert value == "value"


def test_string_blank(example_env):
    value = example_env.get_string("top.string-blank")
    assert value is None


def test_string_stripped(example_env):
    value = example_env.get_string("top.string-whitespace")
    assert value == "foo"


def test_string_stripped_transform(example_env) -> None:
    value: str | None = None

    def _transform(v: str) -> str:
        nonlocal value
        value = v
        return v

    transformed = example_env.get_string("top.string-whitespace", transform=_transform)
    assert transformed == "foo"
    assert value == "foo"


def test_string_defaults_if_blank(example_env):
    value = example_env.get_string("top.string-blank", default="foo")
    assert value == "foo"
