import json
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
sources = json.loads((root / 'research_sources.json').read_text())
ledger = root / '.citation-ledger.json'
skill_script = Path('/opt/data/profiles/researcher/skills/research/grounded-citations/scripts/sources.py')
base_cmd = ['python3', str(skill_script), '--ledger', str(ledger)]
subprocess.run(base_cmd + ['reset'], check=True)
for src in sources:
    cp = subprocess.run(base_cmd + ['add', src['url'], '--title', src['title']], text=True, capture_output=True)
    if cp.returncode != 0:
        print('ADD_FAILED', src['key'], src['url'], cp.stderr.strip())
    else:
        src['citation'] = cp.stdout.strip()
(root / 'research_sources_registered.json').write_text(json.dumps(sources, indent=2) + '\n')
print(f'registered={sum(1 for s in sources if s.get("citation"))} ledger={ledger}')
