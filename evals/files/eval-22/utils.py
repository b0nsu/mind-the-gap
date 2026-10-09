import os
import sys
import json
import re
from datetime import datetime


def parse_ts(value):
    return datetime.fromisoformat(value)


def load_config(path):
    with open(path) as f:
        return json.load(f)
