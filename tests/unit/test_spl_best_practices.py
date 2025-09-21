from pathlib import Path
from tools.parsing import iter_detections
from tools.validators import has_index, has_table, has_stats, has_ttp, has_testing_data

def test_index_and_aggregation():
    """Check each detection SPL has index and uses aggregation."""
    for path, det in iter_detections(Path("detections")):
        spl = det["search"]
        assert has_index(spl), f"{path}: SPL missing index= filter"
        assert has_table(spl) or has_stats(spl), f"{path}: SPL should use table/stats"

def test_ttp_and_testing_data():
    """Check detections have MITRE ATT&CK and testing data tags."""
    for path, det in iter_detections(Path("detections")):
        assert has_ttp(det), f"{path}: missing MITRE ATT&CK mapping"
        assert has_testing_data(det), f"{path}: missing test dataset info"
