from __future__ import annotations

from dataclasses import dataclass

from app.dataclass_utils import from_dict, to_dict


@dataclass
class Settings:
    humidity_setpoint: float = 0.0

    def to_dict(self) -> dict:
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Settings:
        return from_dict(cls, data)
