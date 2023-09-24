from dataclasses import dataclass
from typing import Iterable, Self, cast, overload

from dotenv import dotenv_values


class Env:
    def __init__(self, values: dict[str, str]):
        self._values = values

    @overload
    def get_string(
        self,
        key: str,
        default: str,
    ) -> str:
        pass

    @overload
    def get_string(
        self,
        key: str,
        default: None = None,
    ) -> str | None:
        pass

    def get_string(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        value = self._values.get(key)
        if value is None or not value.strip():
            return default

        return value

    def get_bool(
        self,
        key: str,
        default: bool,
    ) -> bool:
        value = self._values.get(key)
        if value is None:
            return default

        stripped = value.strip()
        if not stripped:
            return default

        return stripped == "true"

    @overload
    def get_int(
        self,
        key: str,
        default: int,
    ) -> int:
        pass

    @overload
    def get_int(
        self,
        key: str,
        default: None = None,
    ) -> int | None:
        pass

    def get_int(
        self,
        key: str,
        default: int | None = None,
    ) -> int | None:
        value = self._values.get(key)
        if value is None or not value.strip():
            return default

        return int(value)

    @overload
    def get_int_list(
        self,
        key: str,
        default: list[int],
    ) -> list[int]:
        pass

    @overload
    def get_int_list(
        self,
        key: str,
        default: None = None,
    ) -> list[int] | None:
        pass

    def get_int_list(
        self,
        key: str,
        default: list[int] | None = None,
    ) -> list[int] | None:
        values = self._values.get(key)

        if values is None or not values.strip():
            return default

        return [int(value) for value in values.split(",")]

