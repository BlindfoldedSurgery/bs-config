from datetime import UTC, date, datetime, time

import pytest

from bs_config.env import Env


@pytest.fixture
def env() -> Env:
    return Env.load_from_dict(
        {
            "ALPHA__BETA_GAMMA": "abc",
            "ALPHA__BETA__GAMMA": "def",
            "UNRELATED": "value",
        }
    )


def test_scoped_div(env):
    scoped = env / "alpha"
    assert scoped.get_string("beta-gamma") == "abc"


def test_empty_prefix_scope(env):
    with pytest.raises(ValueError):
        env / ""


def test_simple_scoped_get(env):
    scoped = env / "alpha"
    assert scoped.get_string("beta-gamma") == "abc"
    assert scoped.get_string("unrelated") is None


def test_nested_scoped_get(env):
    alpha = env / "alpha"
    beta = alpha / "beta"
    assert beta.get_string("gamma") == "def"


def test_original_not_scoped(env):
    scoped = env / "alpha"
    assert env.get_string("unrelated")
    assert env.get_string("alpha.beta-gamma")
    assert scoped.get_string("beta-gamma")


def test_scoped_get_bool():
    env = Env.load_from_dict({"A__B": "True"})
    scoped = env / "a"
    assert scoped.get_bool("b", default=False) is True


def test_scoped_get_int():
    env = Env.load_from_dict({"A__B": "42"})
    scoped = env / "a"
    assert scoped.get_int("b") == 42


def test_scoped_get_string_list():
    env = Env.load_from_dict({"A__B": "a,b,c"})
    scoped = env / "a"
    assert scoped.get_string_list("b") == ["a", "b", "c"]


def test_scoped_get_int_list():
    env = Env.load_from_dict({"A__B": "1,2,3"})
    scoped = env / "a"
    assert scoped.get_int_list("b") == [1, 2, 3]


def test_get_scoped_string_transformed_value():
    env = Env.load_from_dict({"A__B": "1"})
    integer = (env / "a").get_string("b", transform=int)
    assert integer == 1


def test_get_scoped_string_list_transformed_value():
    env = Env.load_from_dict({"A__B": "1,2,3"})
    integers = (env / "a").get_string_list("b", transform=int)
    assert integers == [1, 2, 3]


def test_get_scoped_datetime():
    env = Env.load_from_dict({"A__B": "1970-01-01T00:00:00Z"})
    scoped = env / "a"
    value = scoped.get_datetime("b")
    assert value == datetime(
        1970,
        1,
        1,
        0,
        0,
        0,
        tzinfo=UTC,
    )


def test_get_scoped_time():
    env = Env.load_from_dict({"A__B": "12:34"})
    scoped = env / "a"
    value = scoped.get_time("b")
    assert value == time(12, 34)


def test_get_scoped_date():
    env = Env.load_from_dict({"A__B": "1970-01-01"})
    scoped = env / "a"
    value = scoped.get_date("b")
    assert value == date(1970, 1, 1)
