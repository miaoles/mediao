#!/usr/bin/env python3


from configuration.credentials import *
from configuration.options import *

from pathlib import Path

def get_current_file_path():
	return str(Path(__file__).parent.resolve())
