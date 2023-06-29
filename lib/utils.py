from pathlib import Path
import re
from typing import Iterable


pwd = Path(__file__).parent.parent


def generate_extensions_list(root=pwd / "exts", prefix="exts") -> Iterable[str]:
    for path in root.iterdir():
        if path.is_dir():
            yield from generate_extensions_list(path, f"{prefix}.{path.name}")
        elif path.suffix == ".py":
            module_name = path.name.removesuffix(".py")
            yield f"{prefix}.{module_name}"


_list_pattern = re.compile(r"[,\s]+")


def split_string(s: str, /) -> list[str]:
    """Split string by commas or spaces"""
    return re.split(_list_pattern, s.strip())
