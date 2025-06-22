import json
import os


file1 = 'index/aggregatedByTypeAndPath_Falcon.json'
file2 = 'no_index/aggregatedByTypeAndPath_Falcon.json'

# Carica i due dataset
with open(file1, 'r', encoding='utf-8') as f:
    d1 = json.load(f)
with open(file2, 'r', encoding='utf-8') as f:
    d2 = json.load(f)


diffs = {}  # { eventType: { path: diff (file1 - file2) } }


for event_type in set(d1) | set(d2):
    diffs[event_type] = {}
    
    paths = set(d1.get(event_type, {})) | set(d2.get(event_type, {}))
    for path in paths:
        v1 = d1.get(event_type, {}).get(path, 0.0)
        v2 = d2.get(event_type, {}).get(path, 0.0)
        diff = v1 - v2
        diffs[event_type][path] = diff


out_file = 'time_differences.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(diffs, f, indent=4)

print(f"Differences written to {out_file}")
