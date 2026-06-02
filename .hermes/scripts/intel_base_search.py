#!/usr/bin/env python3
"""Compatibility wrapper for the Git-backed IntelBase helper."""
import runpy
from pathlib import Path

TARGET = Path('/opt/data/HeRmEz/scripts/intelbase_lookup.py')
runpy.run_path(str(TARGET), run_name='__main__')
