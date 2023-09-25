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
        value = self._get_stripped_value(key)
        if value is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return int(value)

    @overload
    def get_int_list(
        self, key: str, *, default: list[int], required: bool = False
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
        values = self._get_stripped_value(key)

        if values is None:
            if default is None and required:
                raise ValueError(f"Missing config value for {key}")
            return default

        return [int(value) for value in values.split(",")]


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
