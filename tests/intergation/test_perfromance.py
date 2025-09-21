import os, pytest
from pathlib import Path
from tools.parsing import iter_detections
from tools.splunk_client import connect
from tools.perf import timed_search

# Configurable thresholds
MAX_RUNTIME_SEC = float(os.getenv("PERF_MAX_RUNTIME_SEC", "15"))
MAX_ROWS = int(os.getenv("PERF_MAX_EVENTS_SCANNED", "2000000"))

@pytest.mark.integration
@pytest.mark.performance
def test_perf_thresholds():
    """Run each detection and check runtime + row limits."""
    svc = connect()
    for path, det in iter_detections(Path("detections")):
        spl = det.get("search", "").strip()
        if not spl:
            pytest.skip(f"{path}: no SPL in detection")
        if "earliest=" not in spl and "latest=" not in spl:
            spl = f"{spl} earliest=-1h latest=now"

        duration, rows = timed_search(svc, spl)
        print(f"[{path}] runtime={duration:.2f}s rows={rows}")

        assert duration <= MAX_RUNTIME_SEC, \
            f"{path}: {duration:.2f}s > {MAX_RUNTIME_SEC}s"
        assert rows <= MAX_ROWS, \
            f"{path}: {rows} rows > {MAX_ROWS}"
