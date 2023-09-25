from typing import Iterable, Literal, cast, overload

from dotenv import dotenv_values


class Env:
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
        value = self._get_stripped_value(key)
        if value is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")

            return default

        return value

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
        value = self._get_stripped_value(key)
        if value is None:
            return default

        return value in ("true", "True", "yes")

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
        value = self._get_stripped_value(key)
        if value is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return int(value)

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
        values = self._get_stripped_value(key)

        if values is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return [stripped for value in values.split(",") if (stripped := value.strip())]

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


def _remove_none_values(data: dict[str, str | None]) -> dict[str, str]:
    for key, value in data.items():
        if value is None:
            del data[key]

    return cast(dict[str, str], data)


def _load_env(name: str | None) -> dict[str, str]:
    # TODO: do we want to load .env always?
    if not name:
        return _remove_none_values(dotenv_values(".env"))
    else:
        return _remove_none_values(dotenv_values(f".env.{name}"))


def load_env(names: Iterable[str]) -> Env:
    result = {**_load_env(None)}

    for name in names:
        result.update(_load_env(name))

    from os import environ

    result.update(environ)

    return Env(result)
