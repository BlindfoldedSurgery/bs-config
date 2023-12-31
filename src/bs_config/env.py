from __future__ import annotations

import abc
from typing import Literal, cast, overload


class Env(abc.ABC):
    @abc.abstractmethod
    def scoped(self, prefix: str) -> Env:
        """
        Args:
            prefix: the prefix to cut off for the scoped instance

        Returns:
            an instance with all key starting with the prefix, now without that prefix
        """
        pass

    @overload
    def get_string(
        self,
        key: str,
        *,
        default: str,
        required: bool = False,
    ) -> str:
        pass

    @overload
    def get_string(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
    ) -> str | None:
        pass

    @overload
    def get_string(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
    ) -> str:
        pass

    @abc.abstractmethod
    def get_string(
        self,
        key: str,
        *,
        default: str | None = None,
        required: bool = False,
    ) -> str | None:
        """
        Get a string value. The value is stripped and blank values are treated as
        missing.

        Args:
            key: the key to look up
            default: a default value, defaults to None
            required: if True, a ValueError is raised instead of returning None

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
    def get_string_list(
        self,
        key: str,
        *,
        default: list[str],
        required: bool = False,
    ) -> list[str]:
        pass

    @overload
    def get_string_list(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[False] = False,
    ) -> list[str] | None:
        pass

    @overload
    def get_string_list(
        self,
        key: str,
        *,
        default: None = None,
        required: Literal[True],
    ) -> list[str]:
        pass

    @abc.abstractmethod
    def get_string_list(
        self,
        key: str,
        *,
        default: list[str] | None = None,
        required: bool = False,
    ) -> list[str] | None:
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
            just be the prefix, so "test" for "test.env". Descending precedence (last
            one wins a conflict).
        """
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

            for additional_dotenv in additional_dotenvs or []:
                values.update(dotenv_values(f"{additional_dotenv}.env"))

        if include_env:
            from os import environ

            values.update(environ)

        return _BaseEnv(cls._remove_none_values(values))

    @classmethod
    def load_from_dict(
        cls,
        values: dict[str, str | None],
    ) -> Env:
        """
        Loads an Env instance using the given values in a dict.
        """
        return _BaseEnv(
            {key: value for key, value in values.items() if value is not None}
        )

    @staticmethod
    def _remove_none_values(data: dict[str, str | None]) -> dict[str, str]:
        for key, value in data.items():
            if value is None:
                del data[key]

        return cast(dict[str, str], data)


class _BaseEnv(Env):
    def __init__(self, values: dict[str, str]):
        self._values = values

    def _get_stripped_value(self, key: str) -> str | None:
        value = self._values.get(key)

        if value is None:
            return value

        value = value.strip()
        if not value:
            return None

        return value

    def scoped(self, prefix: str) -> Env:
        if not prefix:
            return self

        return _ScopedEnv(self, prefix)

    def get_string(  # type: ignore[override]
        self,
        key: str,
        *,
        default: str | None = None,
        required: bool = False,
    ) -> str | None:
        value = self._get_stripped_value(key)
        if value is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")

            return default

        return value

    def get_bool(  # type: ignore[override]
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        value = self._get_stripped_value(key)
        if value is None:
            return default

        return value in ("true", "True", "yes")

    def get_int(  # type: ignore[override]
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        value = self._get_stripped_value(key)
        if value is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return int(value)

    def get_string_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[str] | None = None,
        required: bool = False,
    ) -> list[str] | None:
        values = self._get_stripped_value(key)

        if values is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return [stripped for value in values.split(",") if (stripped := value.strip())]

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        values = self._get_stripped_value(key)

        if values is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        result: list[int] = []
        for value in values.split(","):
            stripped = value.strip()
            if not stripped:
                continue

            try:
                result.append(int(stripped))
            except ValueError:
                raise ValueError(f"Invalid integer for key {key}: '{value}'")

        return result


class _ScopedEnv(Env):
    def __init__(self, parent: Env, prefix: str) -> None:
        self.parent = parent
        self.prefix = prefix

    def scoped(self, prefix: str) -> Env:
        return _ScopedEnv(self, prefix)

    def get_string(  # type: ignore[override]
        self,
        key: str,
        *,
        default: str | None = None,
        required: bool = False,
    ) -> str | None:
        return self.parent.get_string(
            f"{self.prefix}{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_bool(  # type: ignore[override]
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        return self.parent.get_bool(f"{self.prefix}{key}", default=default)

    def get_int(  # type: ignore[override]
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        return self.parent.get_int(
            f"{self.prefix}{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_string_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[str] | None = None,
        required: bool = False,
    ) -> list[str] | None:
        return self.parent.get_string_list(
            f"{self.prefix}{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        return self.parent.get_int_list(
            f"{self.prefix}{key}",
            default=default,  # type: ignore[arg-type]
            required=required,
        )
