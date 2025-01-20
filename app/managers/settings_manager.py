from pathlib import Path

import toml

from app.config.config import Config
from app.settings.settings import Settings


class SettingsManager:
    def __init__(self, config: Config) -> None:
        self.config = config
        project_path = Path(__file__).parent.parent.parent
        self.path = project_path / self.config.settings_path
        self.settings = Settings()

    def load(self) -> None:
        if self.path.is_dir():
            raise IsADirectoryError(f"{self.path} is a directory")
        if not self.path.exists():
            self.save()
            return
        settings_data = toml.load(str(self.path))
        self.settings = Settings.from_dict(settings_data)

    def save(self) -> None:
        with open(self.path, "w") as f:
            f.write(toml.dumps(self.settings.to_dict()))
