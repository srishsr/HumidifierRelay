from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import toml

from app.dataclass_utils import from_dict, to_dict


@dataclass
class Config:
    idle_timeout: float = 60.0
    settings_path: str = "settings.toml"

    def to_dict(self) -> dict:
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Config:
        return from_dict(cls, data)


def load_config(path: Path) -> Config:
    with open(path) as file:
        return Config.from_dict(toml.load(file))
