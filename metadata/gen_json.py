import os
import json

base_dir = "./"
result = {}

for repo_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, repo_name)
    if os.path.isdir(folder_path):
        xml_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".xml")])
        result[repo_name] = xml_files

with open("ebu_cs_file_index.json", "w") as f:
    json.dump(result, f, indent=2)
