from pathlib import Path
from typing import Iterator, Tuple
import yaml

DETECTIONS_DIR = Path("detections")

def load_detection(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def iter_detections(root: Path = DETECTIONS_DIR) -> Iterator[Tuple[Path, dict]]:
    for p in sorted(root.glob("*.yml")):
        yield p, load_detection(p)