from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Literal, cast, overload

if TYPE_CHECKING:
    from collections.abc import Callable

import logging

_logger = logging.getLogger(__name__)


class Env(abc.ABC):
    @abc.abstractmethod
    def __truediv__(self, key: str, /) -> Env:
        """
        Args:
            key: a key to limit the scope to (only one layer at a time)

        Returns:
            an instance that is scoped to the given key

        """
        pass

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

    @classmethod
    def load(
        cls,
        *,
        include_env: bool = True,
        include_default_dotenv: bool = False,
        additional_dotenvs: list[str] | None = None,
    ) -> Env:
        """
        Loads an Env instance.

        Precedence (highest to lowest): ``os.environ``, ``additional_dotenvs``, ``.env``

        **Warning**: To use dotenv functionality, you must install the dotenv extra.

        Args:
            include_env: whether to include the ``os.environ`` variables
            include_default_dotenv: whether to include the ``.env`` file (if it exists)
            additional_dotenvs: a list of other ``.env`` files to include. This should
                just be the prefix, so "test" for "test.env". Ascending precedence (last
                one wins a conflict).
        """
        from ._implementation.default import DefaultEnv
        from ._implementation.direnv import DirenvEnv

        values = {}

        if include_default_dotenv or additional_dotenvs:
            try:
                from dotenv import dotenv_values
            except ImportError as e:
                raise RuntimeError(
                    "dotenv extra is not installed! Use bs-config[dotenv]."
                ) from e

            if include_default_dotenv:
                values.update(dotenv_values(".env"))

            if additional_dotenvs is not None:
                for additional_dotenv in additional_dotenvs:
                    values.update(dotenv_values(f"{additional_dotenv}.env"))

        if include_env:
            from os import environ

            values.update(environ)

        return DirenvEnv(
            DefaultEnv(),
            cls._remove_none_values(values),
        )

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
