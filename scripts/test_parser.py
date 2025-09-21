import os, sys, json
from tools.splunk_client import connect

def parse_only(query: str):
    svc = connect()
    q = query.strip()
    if not (q.startswith("search") or q.startswith("|")):
        q = "search " + q
    resp = svc.post("search/parser", q=q, output_mode="json", parse_only=True)
    payload = json.loads(resp.body.read())
    messages = payload.get("messages", [])
    commands = [c.get("command") for c in payload.get("commands", [])]
    return messages, commands

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else os.getenv("SPL", "index=win sourcetype=XmlWinEventLog:Security EventID=4720 | head 1")
    msgs, cmds = parse_only(q)
    print("Query:", q)
    print("Parser messages:", msgs or "none")
    print("Parsed commands:", cmds or "none")
    if any(m.get("type") == "ERROR" for m in msgs):
        sys.exit(2)