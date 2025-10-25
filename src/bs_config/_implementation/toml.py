import logging
import tomllib
import warnings
from collections.abc import Callable
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Self, cast

from bs_config import Env

_logger = logging.getLogger(__name__)


class TomlEnv(Env):
    def __init__(self, parent: Env, toml_values: dict[str, Any]) -> None:
        self.__parent = parent
        self.__values = toml_values

    @classmethod
    def load_toml_config(cls, parent: Env, toml_config: Path) -> Self | None:
        if not toml_config.is_file():
            return None

        try:
            with toml_config.open("rb") as f:
                content = tomllib.load(f, parse_float=str)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Could not decode TOML config at {toml_config}: %s", e)

        return cls(parent, content)

    def _get_nested_value(self, key: str) -> Any | None:
        if key != key.lower():
            warnings.warn("Keys should use kebab-case")

        if not key:
            raise ValueError("Empty key")

        key_parts = key.split(".")
        value: Any | None = self.__values
        for part in key_parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif value is None:
                return None
            else:
                raise ValueError("Tried to get nested key from scalar value")

        return value

    def _get_stripped_value[T](self, key: str, value_type: type[T]) -> T | None:
        value = self._get_nested_value(key)

        if value is None:
            return value

        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None

        if isinstance(value, value_type):
            return value

        raise ValueError(
            f"Expected value of type {value_type}, but got {type(value)} for key {key}"
        )

    def get_string[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        value = self._get_stripped_value(key, str)
        if value is None:
            return self.__parent.get_string(
                key,
                default=default,
                required=required,
                transform=transform,
            )

        if transform is None:
            return value  # type: ignore[return-value]

        return transform(value)

    def get_bool(  # type: ignore[override]
        self,
        key: str,
        *,
        default: bool,
    ) -> bool:
        value = self._get_stripped_value(key, bool)
        if value is None:
            return self.__parent.get_bool(
                key,
                default=default,
            )

        return value

    def get_int(  # type: ignore[override]
        self,
        key: str,
        *,
        default: int | None = None,
        required: bool = False,
    ) -> int | None:
        value = self._get_stripped_value(key, int)
        if value is None:
            return self.__parent.get_int(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

        return value

    def get_string_list[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        values = self._get_stripped_value(key, list)

        if values is None:
            return self.__parent.get_string_list(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
                transform=transform,
            )

        result: list[T] = []
        for value in values:
            if not isinstance(value, str):
                raise ValueError(
                    f"Got {type(value)} value instead of str in list for key {key}"
                )

            stripped = value.strip()
            if not stripped:
                continue

            if transform is None:
                result.append(cast(T, stripped))
            else:
                result.append(transform(stripped))

        return result

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        values = self._get_stripped_value(key, list)

        if values is None:
            return self.__parent.get_int_list(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

        result: list[int] = []
        for value in values:
            # Not doing isinstance() here because bool is a subtype of int
            if type(value) is not int:
                raise ValueError(f"Got non-int value in list for key {key}")

            result.append(value)

        return result

    def get_datetime(  # type: ignore[override]
        self,
        key: str,
        *,
        default: datetime | None = None,
        required: bool = False,
        is_naive: bool = False,
    ) -> datetime | None:
        value = self._get_stripped_value(key, datetime)
        if value is None:
            return self.__parent.get_datetime(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
                is_naive=is_naive,
            )

        if value.tzinfo is None:
            if is_naive:
                return value

            raise ValueError(
                "Received timezone-aware datetime value, but a naive datetime was expected"
            )
        else:
            if not is_naive:
                return value

            raise ValueError(
                "Received timezone-naive datetime value, but a timezone-aware datetime was expected"
            )

    def get_date(  # type: ignore[override]
        self,
        key: str,
        *,
        default: date | None = None,
        required: bool = False,
    ) -> date | None:
        value = self._get_stripped_value(key, date)
        if value is None:
            return self.__parent.get_date(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

        return value

    def get_time(  # type: ignore[override]
        self,
        key: str,
        *,
        default: time | None = None,
        required: bool = False,
    ) -> time | None:
        value = self._get_stripped_value(key, time)
        if value is None:
            return self.__parent.get_time(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

        if value.tzinfo is not None:
            # Should be impossible to represent in TOML anyway
            raise ValueError(f"Receive timezone-aware time for key {key}")

        return value
