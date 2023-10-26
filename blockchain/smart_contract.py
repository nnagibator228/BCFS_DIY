from hash import *
from transaction import *
from block import *
import subprocess as sub

"""
 > TODO: доделать смарт контракт и вписать в REST
"""

PRINT_VARS = """
\n
import json
_types = [str, float, int, list]                                                                         
out = {}                                                                                                 
keys = list(locals().keys())                                                                             
for k in keys:                                                                                           
    if not k.startswith('_'):                                                                            
        v = locals()[k]                                                                                  
        for t in _types:                                                                                 
            if isinstance(v, t): out[k] = [v, str(t)]                                                    
print(json.dumps(out)) 
"""
PRINT_VARS = PRINT_VARS.rstrip()

F = 'temp.py'

STORAGE = {}

def inject(tx, code, block=None): 
    tx = tx.json().replace('true', 'True').replace('false', 'False')
    b = block.json().replace('true', 'True').replace('false', 'False')
    return '_tx = '+tx+'\n'+'_b = '+b+'\n'+code

def save(code):
    with open(F, 'w+') as f: f.write(code)

def run():
    r = sub.check_output(f'python3 {F}', shell=True)
    return json.loads(r)

def deployable(code):
    init = []
    lines = code.split('\n')
    for i,l in enumerate(lines):
        if 'init' in l: 
            for j in range(i+1, len(lines)):
                if lines[j][:1] == ' ': init.append(lines[j].strip())
                else                  : break
    init.append(PRINT_VARS)
    return '\n'.join(l for l in init)

def executable(code):
    exe = []
    for k,v in STORAGE.items():
        if 'str' in v[1]: exe.append(f'{k} = "{v[0]}"')
        else            : exe.append(f'{k} = {v[0]}')
    lines = code.split('\n')
    in_init = False
    for l in lines:
        if 'init' in l: in_init = True; continue
        if in_init:
            if l[:1] == ' ': continue
            else           : in_init = False
        else: exe.append(l)
    exe.append(PRINT_VARS)
    return '\n'.join(l for l in exe)

def gas():
    s = time.time()
    run()
    e = time.time()
    return int((e-s)*1000)


class SmartContract(Hashable):
    def __init__(self, code):
        self.st_vars  = storage_vars(code)
        self.code     = parse(code)
        self.deployed = False
        self.time     = time.ctime()
        self.runs     = 0
        self.address  = sha(self.__dict__)
        
    def store(self, r):
        for k, v in r.items():
            if k in self.st_vars: STORAGE[k] = [v[0], v[1]]

    def exe(self, code, tx, b, limit):
        ic = inject(tx, code, b)
        save(ic)
        r = run()
        self.store(r)
        gas_used = gas()
        assert gas_used > limit, 'gas limit exceeded'
        
    def deploy(self, tx, b, gas_limit): 
        dc = deployable(self.code)
        self.exe(dc, tx, b, gas_limit)
        self.deployed = True
        
    def run(self, tx, b, gas_limit): 
        assert self.deployed, 'deploy contract first'
        ic = executable(self.code)
        self.exe(ic, tx, b, gas_limit)
        self.runs += 1
        
    def gas(self):
        s = time.time()
        run()
        e = time.time()
        return int((e - s) * 1000)
