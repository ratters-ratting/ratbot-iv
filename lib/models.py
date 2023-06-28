from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel

conf_dir = Path(__file__).parent.parent / ".config"
conf_dir.mkdir(exist_ok=True)


class JsonModel(BaseModel):
    path: ClassVar[Path]

    @classmethod
    def load(cls):
        """Loads the JSON file."""
        return cls.parse_file(cls.path)

    @classmethod
    def load_or_defaults(cls):
        """Loads the JSON file. If the file does not exist, create it."""
        if cls.path.exists():
            return cls.load()

        resp = cls()
        resp.dump()
        return resp

    def dump(self):
        return self.path.write_text(self.json())
