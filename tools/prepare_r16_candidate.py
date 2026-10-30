"""Validate/package R16 into an isolated namespace. Never installs or stages."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import prepare_rocky_candidate as base

ROOT=Path(__file__).resolve().parents[1]
OWN={'main.txt':'scripts/rocky_r16/main.txt',
     'config/Experiments.txt':'scripts/rocky_r16/config/Experiments.txt',
     'combat/Experiments.txt':'scripts/rocky_r16/combat/Experiments.txt',
     'locations/RockyPlateau.txt':'scripts/rocky/locations/RockyPlateau.txt'}

def inspect(root=ROOT):
    root=Path(root)
    baseline=base.inspect(root)
    # Baseline dependencies are required, not installed by this bundle.
    dependencies={k:v for k,v in baseline.items()
                  if not k.startswith('SpeedRunRocky/') or
                  k in {'SpeedRunRocky/config/RockySettings.txt',
                        'SpeedRunRocky/equipment/RockyGear.txt',
                        'SpeedRunRocky/combat/AttackCycle.txt'}}
    data=dict(dependencies)
    data.update({'SpeedRunRockyR16/'+k:(root/v).read_bytes() for k,v in OWN.items()})
    for name in ('SpeedRunRockyR16/'+k for k in OWN):
        text=data[name].decode('utf-8-sig')
        for line in text.splitlines():
            base.require('\t' not in line and (len(line)-len(line.lstrip()))%2==0,
                         'R16 indentation: '+name)
        for dep in re.findall(r'^\s*var \w+ = (?:new|import) ([\w/]+)',text,re.M):
            base.require(dep+'.txt' in data,'Unresolved R16 dependency '+dep)
    main=data['SpeedRunRockyR16/main.txt'].decode()
    actions=data['SpeedRunRockyR16/combat/Experiments.txt'].decode()
    config=data['SpeedRunRockyR16/config/Experiments.txt'].decode()
    base.require('rocky.experiment = extras' in main and main.count('extras.Prepare(extraConfig)')==3,
                 'R16 attachment/preparation missing')
    base.require('var maskEnabled = false' in config and 'var dashEnabled = false' in config,
                 'R16 features must default off')
    base.require('GetCount("debuff_' not in actions and 'activate potion' not in actions,
                 'Unverified effect UID/potion policy introduced')
    base.require(len(re.findall(r'^\s+activate R$', actions, re.M))==1, 'Expected one protected activation site')
    # Preserve the successful baseline defense literally, not just its thresholds.
    base.require('var rayDodgeTriggerFrame = 23' in data['SpeedRunRocky/config/RockySettings.txt'].decode(),
                 'Ray trigger changed')
    return data

def prepare(root=ROOT):
    root=Path(root);data=inspect(root)
    manifest={'format_version':1,'candidate':'R16 EXPERIMENTAL, NOT DEPLOYED OR GAME VERIFIED',
              'base':'5d57ccf (gameplay 1c696fe)',
              'files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(data.items())},
              'sources':{'SpeedRunRockyR16/'+k:v for k,v in OWN.items()}}
    raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
    folder=root/'artifacts/rocky-r16'/hashlib.sha256(raw).hexdigest()
    payload={'manifest.json':raw,**{k:v for k,v in data.items() if k.startswith('SpeedRunRockyR16/')}}
    if folder.exists():
        base.require(all((folder/k).is_file() and (folder/k).read_bytes()==v for k,v in payload.items()),
                     'Existing immutable R16 bundle differs')
    else:
        for name,value in payload.items():
            p=folder/name;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f:f.write(value)
    return folder

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true')
    args=parser.parse_args()
    files=inspect()
    if args.prepare:print('Prepared:',prepare().relative_to(ROOT))
    print('PASS:',len(files),'manifest files; four R16-only payload files; no installation')
