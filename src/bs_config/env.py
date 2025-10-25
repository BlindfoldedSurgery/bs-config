from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Literal, cast, overload

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from datetime import date, datetime, time
    from pathlib import Path

from datetime import timedelta


class Env(abc.ABC):
    def __truediv__(self, key: str, /) -> Env:
        """
        Args:
            key: a key to limit the scope to (only one layer at a time)

        Returns:
            an instance that is scoped to the given key

        """
        from ._implementation.scoped import ScopedEnv

        if not key:
            raise ValueError("Key cannot be empty")

        return ScopedEnv(self, key)

    @overload
    def get_string[T = str](
        self,
        key: str,
        *,
        default: T,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T:
        pass

    @overload
    def get_string[T = str](
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        pass

    @overload
    def get_string[T = str](
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
        transform: Callable[[str], T] | None = None,
    ) -> T:
        pass

    @overload
    def get_string[T = str](
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        pass

    @abc.abstractmethod
    def get_string[T = str](
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        """
        Get a string value. The value is stripped and blank values are treated as
        missing.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None
            transform: a function to transform non-blank values

        Returns:
            The requested value, or the default value
        """
        pass

    @abc.abstractmethod
    def get_bool(
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        """
        Get a bool value. The original string value is stripped, and then 'true',
        'True', and 'yes' are treated as True. ALL other non-blank strings are treated
        as False.

        Args:
            key: the key to look up
            default: a default value, defaults to False

        Returns:
            The requested value, or the default value if the value is missing or blank.
        """
        pass

    @overload
    def get_int(
        self,
        key: str,
        *,
        default: int,
        required: bool = False,
    ) -> int:
        pass

    @overload
    def get_int(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
    ) -> int | None:
        pass

    @overload
    def get_int(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
    ) -> int:
        pass

    @overload
    def get_int(
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        pass

    @abc.abstractmethod
    def get_int(
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        """
        Get an int value.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None

        Returns:
            The requested value, or the default value

        Raises:
            ValueError: 1) If the value is not a valid int. 2) If the value is missing,
                the default is None, and required is True.
        """
        pass

    @overload
    def get_string_list[T = str](
        self,
        key: str,
        *,
        default: list[T],
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T]:
        pass

    @overload
    def get_string_list[T = str](
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        pass

    @overload
    def get_string_list[T = str](
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
        transform: Callable[[str], T] | None = None,
    ) -> list[T]:
        pass

    @overload
    def get_string_list[T = str](
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        pass

    @abc.abstractmethod
    def get_string_list[T = str](
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        """
        Gets a list of strings, splitting the original value by comma. For each value,
        the same rules as for ``get_string`` apply. Blank values are discarded.

        Note that a blank string is treated as a missing value, so it will trigger a
        fallback to the default value. If you want an empty list, use "," (technically
        a list of two blank values, but blank values are discarded).

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None
            transform: a function to transform each list item

        Returns:
            a list of strings parsed from the value, or the default value

        """
        pass

    @overload
    def get_int_list(
        self,
        key: str,
        *,
        default: list[int],
        required: bool = False,
    ) -> list[int]:
        pass

    @overload
    def get_int_list(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
    ) -> list[int] | None:
        pass

    @overload
    def get_int_list(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
    ) -> list[int]:
        pass

    @overload
    def get_int_list(
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        pass

    @abc.abstractmethod
    def get_int_list(
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        """
        Gets a list of ints, splitting the original value by comma. For each value,
        the same rules as for ``get_int`` apply. Blank values are discarded.

        Note that a blank string is treated as a missing value, so it will trigger a
        fallback to the default value. If you want an empty list, use "," (technically
        a list of two blank values, but blank values are discarded).

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None

        Returns:
            a list of ints parsed from the value, or the default value
        """
        pass

    @overload
    def get_datetime(
        self,
        key: str,
        *,
        default: datetime,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime:
        pass

    @overload
    def get_datetime(
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: Literal[False] = False,
        is_naive: bool = False,
    ) -> datetime | None:
        pass

    @overload
    def get_datetime(
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: Literal[True],
        is_naive: bool = False,
    ) -> datetime:
        pass

    @overload
    def get_datetime(
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime | None:
        pass

    @abc.abstractmethod
    def get_datetime(
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime | None:
        """
        Get a datetime value.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None
            is_naive: if True, a timezone-naive datetime is expected, otherwise
               a timezone-aware datetime is expected

        Returns:
            The requested value, or the default value

        Raises:
            ValueError:
                1. If the value is not a valid ISO8601 datetime.

                2. If the datetime is timezone-naive but is_naive is False, or the
                other way around.

                3. The supplied default value does not match the is_naive argument.

                3. If the value is missing,
                the default is None, and required is True.
        """
        pass

    @overload
    def get_date(
        self,
        key: str,
        *,
        default: date,
        required: bool = False,
    ) -> date:
        pass

    @overload
    def get_date(
        self,
        key: str,
        *,
        default: date | None = None,
        required: Literal[False] = False,
    ) -> date | None:
        pass

    @overload
    def get_date(
        self,
        key: str,
        *,
        default: date | None = None,
        required: Literal[True],
    ) -> date:
        pass

    @overload
    def get_date(
        self,
        key: str,
        *,
        default: date | None = None,
        required: bool = False,
    ) -> date | None:
        pass

    @abc.abstractmethod
    def get_date(
        self,
        key: str,
        *,
        default: date | None = None,
        required: bool = False,
    ) -> date | None:
        """
        Get a date value.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None

        Returns:
            The requested value, or the default value

        Raises:
            ValueError:
                1. If the value is not a valid ISO8601 date.
                2. If the value is missing,
                the default is None, and required is True.
        """
        pass

    @overload
    def get_time(
        self,
        key: str,
        *,
        default: time,
        required: bool = False,
    ) -> time:
        pass

    @overload
    def get_time(
        self,
        key: str,
        *,
        default: time | None = None,
        required: Literal[False] = False,
    ) -> time | None:
        pass

    @overload
    def get_time(
        self,
        key: str,
        *,
        default: time | None = None,
        required: Literal[True],
    ) -> time:
        pass

    @overload
    def get_time(
        self,
        key: str,
        *,
        default: time | None = None,
        required: bool = False,
    ) -> time | None:
        pass

    @abc.abstractmethod
    def get_time(
        self,
        key: str,
        *,
        default: time | None = None,
        required: bool = False,
    ) -> time | None:
        """
        Get a time value.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None

        Returns:
            The requested value, or the default value

        Raises:
            ValueError:
                1. If the value is not a valid ISO8601 time.
                2. If the time is timezone-aware.
                3. If the default value is timezone-aware.
                4. If the value is missing,
                the default is None, and required is True.
        """
        pass

    @overload
    def get_duration(
        self,
        key: str,
        *,
        default: timedelta,
        required: bool = False,
    ) -> timedelta:
        pass

    @overload
    def get_duration(
        self,
        key: str,
        *,
        default: timedelta | None = None,
        required: Literal[True],
    ) -> timedelta:
        pass

    @overload
    def get_duration(
        self,
        key: str,
        *,
        default: timedelta | None = None,
        required: Literal[False] = False,
    ) -> timedelta | None:
        pass

    @overload
    def get_duration(
        self,
        key: str,
        *,
        default: timedelta | None = None,
        required: bool = False,
    ) -> timedelta | None:
        pass

    def get_duration(
        self,
        key: str,
        *,
        default: timedelta | None = None,
        required: bool = False,
    ) -> timedelta | None:
        """
        Get a duration value (as timedelta). If the underlying format (like env or TOML)
        doesn't have a native way to represent a duration, the key serves as a scope and
        the parts of timedelta are looked up within that scope.

        So if you look up the key "my-duration", it's roughly the equivalent of::

            scoped = env / "my-duration"
            return timedelta(
                weeks=scoped.get_int("weeks", default=0),
                days=scoped.get_int("days", default=0),
                hours=scoped.get_int("hours", default=0),
                minutes=scoped.get_int("minutes", default=0),
                seconds=scoped.get_int("seconds", default=0),
                milliseconds=scoped.get_int("milliseconds", default=0),
                microseconds=scoped.get_int("microseconds", default=0)
            )

        Args:
            key: the key to look up
            default: a default value in case none of the timedelta fields were
                explicitly set, defaults to None
            required: if True, a ValueError is raised instead of returning None

        Returns:
            The requested value, or the default value

        Raises:
            ValueError:
                1. Any supplied value was not a valid int
                2. No subfield was set, no default was given, but required is True
        """
        scoped = self / key

        # First get all parts as optional to allow us to differentiate 0 and None
        weeks = scoped.get_int("weeks")
        days = scoped.get_int("days")
        hours = scoped.get_int("hours")
        minutes = scoped.get_int("minutes")
        seconds = scoped.get_int("seconds")
        milliseconds = scoped.get_int("milliseconds")
        microseconds = scoped.get_int("microseconds")

        is_unset = all(
            v is None
            for v in [weeks, days, hours, minutes, seconds, milliseconds, microseconds]
        )

        if is_unset:
            if required and default is None:
                raise ValueError(f"Missing duration under scope-key {key}")

            return default

        return timedelta(
            weeks=weeks or 0,
            days=days or 0,
            hours=hours or 0,
            minutes=minutes or 0,
            seconds=seconds or 0,
            milliseconds=milliseconds or 0,
            microseconds=microseconds or 0,
        )

    @classmethod
    def load(
        cls,
        *,
        include_env: bool = True,
        include_default_dotenv: bool = False,
        additional_dotenvs: Iterable[str] | None = None,
        toml_configs: Iterable[Path] | None = None,
    ) -> Env:
        """
        Loads an Env instance.

        Precedence (highest to lowest): ``os.environ``, ``additional_dotenvs``,
            ``.env``, ``toml_configs``

        **Warning**: To use dotenv functionality, you must install the dotenv extra.

        Args:
            include_env: whether to include the ``os.environ`` variables
            include_default_dotenv: whether to include the ``.env`` file (if it exists)
            additional_dotenvs: a list of other ``.env`` files to include. This should
                just be the prefix, so "test" for "test.env". Ascending precedence (last
                one wins a conflict).
            toml_configs: a list of ``.toml`` files to include. It's not an error if
                the files do not exist. Keys in TOML should be kebab-case and will be
                normalized to screaming snake case.
                Ascending precedence (last one wins a conflict).
        """
        from ._implementation.default import DefaultEnv
        from ._implementation.direnv import DirenvEnv
        from ._implementation.toml import TomlEnv

        result: Env = DefaultEnv()

        if toml_configs is not None:
            for toml_config in toml_configs:
                toml_env = TomlEnv.load_toml_config(result, toml_config)
                if toml_env is not None:
                    result = toml_env

        if include_default_dotenv or (additional_dotenvs is not None):
            try:
                from dotenv import dotenv_values
            except ImportError as e:
                raise RuntimeError(
                    "dotenv extra is not installed! Use bs-config[dotenv]."
                ) from e

            if include_default_dotenv:
                values = dotenv_values(".env")
                if values:
                    result = DirenvEnv(result, cls._remove_none_values(values))

            if additional_dotenvs is not None:
                for additional_dotenv in additional_dotenvs:
                    values = dotenv_values(f"{additional_dotenv}.env")
                    if values:
                        result = DirenvEnv(result, cls._remove_none_values(values))

        if include_env:
            from os import environ

            result = DirenvEnv(result, cls._remove_none_values(dict(environ)))

        return result

    @classmethod
    def load_from_dict(
        cls,
        values: dict[str, str | None],
    ) -> Env:
        """
        Loads an Env instance using the given values in a dict.
        """
        from ._implementation.default import DefaultEnv
        from ._implementation.direnv import DirenvEnv

        return DirenvEnv(
            DefaultEnv(),
            {key: value for key, value in values.items() if value is not None},
        )

    @staticmethod
    def _remove_none_values(data: dict[str, str | None]) -> dict[str, str]:
        none_keys = []
        for key, value in data.items():
            if value is None:
                none_keys.append(key)

        for key in none_keys:
            del data[key]

        return cast(dict[str, str], data)
