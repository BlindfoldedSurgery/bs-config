import warnings
from collections.abc import Callable

from bs_config import Env

from .scoped import ScopedEnv


class DirenvEnv(Env):
    def __init__(self, parent: Env, values: dict[str, str]) -> None:
        self.__parent = parent
        self._values = values

    @staticmethod
    def _to_screaming_snake_case(s: str) -> str:
        return s.replace("-", "_").upper()

    def _get_stripped_value(self, key: str) -> str | None:
        if key != key.lower():
            warnings.warn("Keys should use kebab-case")

        key_parts = key.split(".")
        full_key = "__".join(self._to_screaming_snake_case(part) for part in key_parts)
        value = self._values.get(full_key)

        if value is None:
            return value

        value = value.strip()
        if not value:
            return None

        return value

    def __truediv__(self, key: str, /) -> Env:
        return ScopedEnv(self, key)

    def get_string[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: T | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> T | None:
        value = self._get_stripped_value(key)
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
        value = self._get_stripped_value(key)
        if value is None:
            return self.__parent.get_bool(
                key,
                default=default,
            )

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
            return self.__parent.get_int(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

        return int(value)

    def get_string_list[T = str](  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[T] | None = None,
        required: bool = False,
        transform: Callable[[str], T] | None = None,
    ) -> list[T] | None:
        values = self._get_stripped_value(key)

        if values is None:
            return self.__parent.get_string_list(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
                transform=transform,
            )

        raw_values = (
            stripped for value in values.split(",") if (stripped := value.strip())
        )
        if transform is None:
            return list(raw_values)  # type: ignore[arg-type]

        return [transform(value) for value in raw_values]

    def get_int_list(  # type: ignore[override]
        self,
        key: str,
        *,
        default: list[int] | None = None,
        required: bool = False,
    ) -> list[int] | None:
        values = self._get_stripped_value(key)

        if values is None:
            return self.__parent.get_int_list(
                key,
                default=default,  # type: ignore[arg-type]
                required=required,
            )

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
