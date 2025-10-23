import pytest

from bs_config.env import Env


@pytest.fixture
def env() -> Env:
    return Env.load_from_dict(
        {
            "ALPHA_BETA_GAMMA": "abc",
            "unrelated": "value",
        }
    )


def test_empty_prefix_scope(env):
    scoped = env.scoped("")
    assert scoped is env


def test_simple_scoped_get(env):
    scoped = env.scoped("ALPHA_")
    assert scoped.get_string("BETA_GAMMA") == "abc"
    assert scoped.get_string("unrelated") is None


def test_nested_scoped_get(env):
    alpha = env.scoped("ALPHA_")
    beta = alpha.scoped("BETA_")
    assert beta.get_string("GAMMA") == "abc"


def test_original_not_scoped(env):
    scoped = env.scoped("ALPHA_")
    assert env.get_string("unrelated")
    assert env.get_string("ALPHA_BETA_GAMMA")
    assert scoped.get_string("BETA_GAMMA")


def test_scoped_get_bool():
    env = Env.load_from_dict({"ab": "True"})
    scoped = env.scoped("a")
    assert scoped.get_bool("b", default=False) is True


def test_scoped_get_int():
    env = Env.load_from_dict({"ab": "42"})
    scoped = env.scoped("a")
    assert scoped.get_int("b") == 42


def test_scoped_get_string_list():
    env = Env.load_from_dict({"ab": "a,b,c"})
    scoped = env.scoped("a")
    assert scoped.get_string_list("b") == ["a", "b", "c"]


def test_scoped_get_int_list():
    env = Env.load_from_dict({"ab": "1,2,3"})
    scoped = env.scoped("a")
    assert scoped.get_int_list("b") == [1, 2, 3]
