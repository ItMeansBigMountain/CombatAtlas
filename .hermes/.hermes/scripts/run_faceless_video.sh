#!/bin/bash
# Wrapper for faceless-youtube-channel daily video generation
# Runs from ~/.hermes/scripts/ but executes the project script with correct working directory

cd /opt/data/HeRmEz/projects/faceless-youtube-channel
python3 scripts/run_trend_video.py --dry-run-upload