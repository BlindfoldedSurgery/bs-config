from datetime import UTC, date, datetime, time, timedelta, timezone

import pytest

from bs_config.env import Env


@pytest.fixture
def env() -> Env:
    return Env.load_from_dict(
        {
            "STRING": "abc",
            "STRING_TRAILING": " abc ",
            "INT": "42",
            "INT_TRAILING": " 42 ",
            "DATE": "1970-01-01",
            "DATE_TRAILING": " 1970-01-01 ",
            "DATETIME_UTC": "1970-01-01T12:34:56Z",
            "DATETIME_TRAILING": " 1970-01-01T12:34:56Z ",
            "DATETIME_AWARE": "1970-01-01T12:34:56+02:30",
            "DATETIME_NAIVE": "1970-01-01T12:34:56",
            "TIME": "12:34",
            "TIME_TRAILING": " 12:34 ",
            "TIME_SECONDS": "12:34:56",
            "EMPTY": "",
            "BLANK": "  ",
        }
    )


@pytest.mark.parametrize(
    "key",
    ["string", "string-trailing"],
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
    ["empty", "blank", "missing-key"],
)
def test_get_string_missing_no_default_required(env, key):
    with pytest.raises(ValueError, match=key):
        env.get_string(key, default=None, required=True)


@pytest.mark.parametrize(
    "default",
    [
        None,
        "test",
        "",
    ],
)
def test_get_string_value_default(env, default):
    value = env.get_string("missing", default=default)
    assert value == default


def test_get_string_value_required_with_default(env):
    value = env.get_string("missing", default="test", required=True)
    assert value == "test"


@pytest.mark.parametrize(
    "raw_value,expected",
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
def test_get_bool_value(raw_value, expected):
    env = Env.load_from_dict({"KEY": raw_value})
    value = env.get_bool("key", default=not expected)
    assert value == expected, f"Value '{raw_value}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_empty_bool_value(value):
    env = Env.load_from_dict({"KEY": value})
    value = env.get_bool("key", default=True)
    assert value is True, f"Value '{value}' does not trigger default value"


@pytest.mark.parametrize(
    "key",
    ["int", "int-trailing"],
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
    with pytest.raises(ValueError, match="missing-key"):
        env.get_int("missing-key", default=None, required=True)


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
    env = Env.load_from_dict({"KEY": value})
    result = env.get_string_list("key")

    assert result == expected, f"'{value}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_string_list_blank(value):
    env = Env.load_from_dict({"KEY": value})
    result = env.get_string_list("key")
    assert result is None


def test_get_string_list_missing_required():
    key = "key"
    env = Env.load_from_dict({})
    with pytest.raises(ValueError, match=key):
        env.get_string_list(key, required=True)


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_string_list_blank_required(value):
    key = "key"
    env = Env.load_from_dict({key: value})
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
    env = Env.load_from_dict({"KEY": value})
    result = env.get_int_list("key")

    assert result == expected, f"'{value}' is not parsed as {expected}"


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_int_list_blank(value):
    env = Env.load_from_dict({"KEY": value})
    result = env.get_int_list("key")
    assert result is None


def test_get_int_list_missing_required():
    key = "key"
    env = Env.load_from_dict({})
    with pytest.raises(ValueError, match=key):
        env.get_int_list(key, required=True)


@pytest.mark.parametrize(
    "value",
    ["", " "],
)
def test_get_int_list_blank_required(value):
    env = Env.load_from_dict({"KEY": value})
    with pytest.raises(ValueError, match="key"):
        env.get_int_list("key", required=True)


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
    key = "key"
    env = Env.load_from_dict({key.upper(): value})
    with pytest.raises(ValueError, match=key):
        env.get_int_list(key)


class _Stub:
    pass


def test_get_string_transformed_value(env):
    integer = env.get_string("int", transform=int)
    assert integer == 42


def test_get_string_transformed_value__default(env, mocker):
    mock = mocker.Mock()
    default = _Stub()
    value = env.get_string("invalid", transform=mock, default=default)
    assert value is default
    mock.assert_not_called()


def test_get_string_transform_not_called_with_none(env, mocker):
    mock = mocker.Mock()
    value = env.get_string("invalid", transform=mock)
    assert value is None
    mock.assert_not_called()


def test_get_string_list_transformed_value():
    env = Env.load_from_dict({"FOO": "1,2,3"})
    integers = env.get_string_list("foo", transform=int)
    assert integers == [1, 2, 3]


def test_get_string_list_transformed_value__default(env, mocker):
    mock = mocker.Mock()
    default = [_Stub()]
    value = env.get_string_list("invalid", transform=mock, default=default)
    assert value is default
    mock.assert_not_called()


def test_get_string_list_transform_not_called_with_none(env, mocker):
    mock = mocker.Mock()
    value = env.get_string_list("invalid", transform=mock)
    assert value is None
    mock.assert_not_called()


@pytest.mark.parametrize(
    "key",
    ["date", "date-trailing"],
)
def test_get_date_value(env, key):
    value = env.get_date(key)
    assert value == date(1970, 1, 1)


def test_get_invalid_date(env):
    with pytest.raises(ValueError):
        env.get_date("string")


@pytest.mark.parametrize(
    "default",
    [
        None,
        date(2000, 1, 1),
    ],
)
def test_get_date_value_default(env, default):
    value = env.get_date("missing", default=default)
    assert value == default


def test_get_date_value_required_with_default(env):
    value = env.get_date(
        "missing",
        default=date(2000, 1, 1),
        required=True,
    )
    assert value == date(2000, 1, 1)


def test_get_date_value_required_no_default(env):
    with pytest.raises(ValueError, match="missing-key"):
        env.get_date("missing-key", default=None, required=True)


@pytest.mark.parametrize(
    "key,expected",
    [
        ("time", time(12, 34)),
        ("time-trailing", time(12, 34)),
        ("time-seconds", time(12, 34, 56)),
    ],
)
def test_get_time_value(env, key, expected):
    value = env.get_time(key)
    assert value == expected


def test_get_invalid_time(env):
    with pytest.raises(ValueError):
        env.get_time("string")


def test_get_time_tz_aware():
    env = Env.load_from_dict({"TZ_TIME": "12:34:56+01:00"})
    with pytest.raises(ValueError):
        env.get_time("tz-time")


@pytest.mark.parametrize(
    "default",
    [
        None,
        time(12, 34),
    ],
)
def test_get_time_value_default(env, default):
    value = env.get_time("missing", default=default)
    assert value == default


@pytest.mark.parametrize(
    "key",
    [
        "missing",
        "time",
    ],
)
def get_time_value_default_aware(env, key):
    with pytest.raises(ValueError):
        env.get_time(
            key,
            default=time(12, 34, 56, tzinfo=UTC),
        )


def test_get_time_required_with_default(env):
    value = env.get_time(
        "missing",
        default=time(12, 34),
        required=True,
    )
    assert value == time(12, 34)


def test_get_time_value_required_no_default(env):
    with pytest.raises(ValueError, match="missing-key"):
        env.get_time("missing-key", default=None, required=True)


@pytest.mark.parametrize(
    "key,expected",
    [
        ("datetime-utc", datetime(1970, 1, 1, 12, 34, 56, tzinfo=UTC)),
        ("datetime-trailing", datetime(1970, 1, 1, 12, 34, 56, tzinfo=UTC)),
        (
            "datetime-aware",
            datetime(
                1970, 1, 1, 12, 34, 56, tzinfo=timezone(timedelta(hours=2, minutes=30))
            ),
        ),
        ("datetime-naive", datetime(1970, 1, 1, 12, 34, 56)),
    ],
)
def test_get_datetime_value(env, key, expected):
    value = env.get_datetime(
        key,
        is_naive=expected.tzinfo is None,
    )
    assert value == expected
    assert value.tzinfo == expected.tzinfo


def test_get_invalid_datetime(env):
    with pytest.raises(ValueError):
        env.get_datetime("string")


@pytest.mark.parametrize(
    "value,is_naive",
    [
        ("1970-01-01T00:00:00Z", True),
        ("1970-01-01T00:00:00+00:00", True),
        ("1970-01-01T00:00:00+01:00", True),
        ("1970-01-01T00:00:00", False),
    ],
)
def test_get_datetime_tz_aware(value, is_naive):
    env = Env.load_from_dict({"DATETIME": value})
    with pytest.raises(ValueError):
        env.get_datetime("datetime", is_naive=is_naive)


@pytest.mark.parametrize(
    "default",
    [
        None,
        datetime(1970, 1, 1, 12, 34, tzinfo=UTC),
    ],
)
def test_get_datetime_value_default_aware(env, default):
    value = env.get_datetime("missing", default=default, is_naive=False)
    assert value == default


@pytest.mark.parametrize(
    "default",
    [
        None,
        datetime(1970, 1, 1, 12, 34),
    ],
)
def test_get_datetime_value_default_naive(env, default):
    value = env.get_datetime("missing", default=default, is_naive=True)
    assert value == default


@pytest.mark.parametrize(
    "key,default",
    [
        ("missing", datetime(1970, 1, 1, 12, 34)),
        ("missing", datetime(1970, 1, 1, 12, 34, tzinfo=UTC)),
    ],
)
def test_get_datetime_value_default_naive_mismatch(env, key, default):
    with pytest.raises(ValueError):
        default_is_naive = default.tzinfo is None
        env.get_datetime(
            key,
            default=default,
            is_naive=not default_is_naive,
        )


def test_get_datetime_required_with_default(env):
    value = env.get_datetime(
        "missing",
        default=datetime(1970, 1, 1, 12, 34, tzinfo=UTC),
        required=True,
    )
    assert value == datetime(1970, 1, 1, 12, 34, tzinfo=UTC)


def test_get_datetime_value_required_no_default(env):
    with pytest.raises(ValueError, match="missing-key"):
        env.get_datetime("missing-key", default=None, required=True)


def test_get_duration_unset_required():
    env = Env.load_from_dict({})
    with pytest.raises(ValueError):
        env.get_duration("missing", required=True)


def test_get_duration_unset_not_required():
    env = Env.load_from_dict({})
    value = env.get_duration("missing")
    assert value is None


def test_get_duration_unset_default():
    env = Env.load_from_dict({})
    default = timedelta(hours=1)
    value = env.get_duration("missing", default=default)
    assert value is default


def test_get_duration_blank_default():
    env = Env.load_from_dict({"TIME__SECONDS": "  "})
    default = timedelta(hours=1)
    value = env.get_duration("time", default=default)
    assert value is default


@pytest.mark.parametrize(
    "seconds",
    [
        20,
        0,
    ],
)
def test_get_duration_partially_set(seconds):
    env = Env.load_from_dict({"TIME__SECONDS": str(seconds)})
    value = env.get_duration("time", required=True)
    assert value == timedelta(seconds=seconds)


def test_get_duration_fully_set():
    env = Env.load_from_dict(
        {
            "TIME__WEEKS": "1",
            "TIME__DAYS": "2",
            "TIME__HOURS": "3",
            "TIME__MINUTES": "4",
            "TIME__SECONDS": "5",
            "TIME__MILLISECONDS": "6",
            "TIME__MICROSECONDS": "107",
        }
    )
    value = env.get_duration("time", required=True)
    assert value == timedelta(
        weeks=1,
        days=2,
        hours=3,
        minutes=4,
        seconds=5,
        milliseconds=6,
        microseconds=107,
    )


def test_get_duration_fully_set_all_zero():
    env = Env.load_from_dict(
        {
            "TIME__WEEKS": "0",
            "TIME__DAYS": "0",
            "TIME__HOURS": "0",
            "TIME__MINUTES": "0",
            "TIME__SECONDS": "0",
            "TIME__MILLISECONDS": "0",
            "TIME__MICROSECONDS": "0",
        }
    )
    value = env.get_duration("time", required=True)
    assert value == timedelta()
