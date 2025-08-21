import json


def load_logs(file_paths, date_filter=None):
    logs = []
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if date_filter:
                        if not entry.get("@timestamp", "").startswith(date_filter):
                            continue
                    logs.append(entry)
                except json.JSONDecodeError:
                    continue
    return logs
