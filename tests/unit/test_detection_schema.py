from pathlib import Path
from tools.parsing import iter_detections

REQUIRED = ["name", "id", "version", "search", "tags"]

def test_top_level_fields_present():
    """Check each detection YAML has required fields."""
    det_dir = Path("detections")
    assert det_dir.exists(), "detections/ folder missing"
    for path, det in iter_detections(det_dir):
        for key in REQUIRED:
            assert key in det, f"{path}: missing required field '{key}'"
        assert isinstance(det["search"], str) and det["search"].strip(), f"{path}: empty search string"
        
test_top_level_fields_present()

