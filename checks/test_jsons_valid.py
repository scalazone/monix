import os
import json
from pathlib import Path
from envs import CONTENT_PATH


def test_jsons_valid():
  for subdir, _, files in os.walk(CONTENT_PATH):
    for file in files:
      filepath = subdir + os.sep + file
      if filepath.endswith(".json"):
        file_text = Path(filepath).read_text()
        try:
          json.loads(file_text)
        except ValueError as e:
          assert False, f"File {file} is not valid json, cause: {repr(e)}"
