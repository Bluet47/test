import os, time
import splunklib.client as client

def connect(host=None, port=None, username=None, password=None, scheme=None, verify=True, retries=5, backoff=2.0):
    host = host or os.getenv("SPLUNK_HOST", "localhost")
    port = int(port or os.getenv("SPLUNK_PORT", "8089"))
    username = username or os.getenv("SPLUNK_USERNAME", "admin")
    password = password or os.getenv("SPLUNK_PASSWORD", "github variable")
    scheme = scheme or os.getenv("SPLUNK_SCHEME", "https")
    app = os.getenv("SPLUNK_APP", "search")
    owner = os.getenv("SPLUNK_OWNER", "nobody")
    verify_env = str(os.getenv("SPLUNK_VERIFY", str(verify))).lower() in ("1","true","yes")

    last_err = None
    for attempt in range(1, retries+1):
        try:
            kwargs = dict(host=host, port=port, username=username, password=password,
                          scheme=scheme, app=app, owner=owner)
            if not verify_env:
                kwargs["verify"] = False
            svc = client.connect(**kwargs)
            _ = list(svc.indexes)  # auth check
            return svc
        except Exception as e:
            last_err = e
            time.sleep(backoff * attempt)
    raise RuntimeError(f"Failed to connect to Splunk after {retries} attempts: {last_err}")