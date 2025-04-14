import yaml
import copy

DEFAULT_BALANCE_DATA = {
    "_nation": "default",
    "treasury": {
        "sovereign": 0,
    },
    "stocks": {
        "DLTA": 0
    },
    "stash": {
        "arm": 0,
        "aut": 0,
        "bas": 0,
        "bev": 0,
        "boo": 0,
        "che": 0,
        "fur": 0,
        "gam": 0,
        "inf": 0,
        "ins": 0,
        "min": 0,
        "piz": 0,
        "ret": 0,
        "tim": 0,
        "tro": 0
    },
}


DEFAULT_STATS_DATA = {
    "_nation": "default",
    "econ": {
        "population": 0,
        "production": 0,
        "private": 0,
        "public": 0,
        "illegal": 0,
        "business": {
            "arm": 0,
            "aut": 0,
            "bas": 0,
            "bev": 0,
            "boo": 0,
            "che": 0,
            "fur": 0,
            "gam": 0,
            "inf": 0,
            "ins": 0,
            "min": 0,
            "piz": 0,
            "ret": 0,
            "tim": 0,
            "tro": 0,
            "sum": 0
        },
        "government": {
            "adm": 0,
            "aid": 0,
            "com": 0,
            "def": 0,
            "edu": 0,
            "enf": 0,
            "env": 0,
            "hea": 0,
            "soc": 0,
            "spi": 0,
            "tra": 0,
            "wel": 0,
            "sum": 0
        }
    }
}

def float_representer(dumper, value):
    text = f"{value:.2f}"
    return dumper.represent_scalar('tag:yaml.org,2002:float', text)

yaml.add_representer(float, float_representer)

balance_yaml = './scripts/data/balance.yaml'
stats_yaml = './scripts/data/stats.yaml'
nations_txt = './scripts/nations.txt'

with open(nations_txt, 'r') as file:
    txt_nations = {line.strip() for line in file if line.strip()}

try:
    with open(balance_yaml, 'r') as f:
        balance_data = yaml.safe_load(f) or {'nations': []}
except FileNotFoundError:
    balance_data = {'nations': []}

try:
    with open(stats_yaml, 'r') as f:
        stats_data = yaml.safe_load(f) or {'nations': []}
except FileNotFoundError:
    stats_data = {'nations': []}

existing_balance_nations = {item['_nation'] for item in balance_data['nations']}
existing_stats_nations = {item['_nation'] for item in stats_data['nations']}

missing_balance_nations = txt_nations - existing_balance_nations
missing_stats_nations = txt_nations - existing_stats_nations

for nation in missing_balance_nations:
    new_entry = copy.deepcopy(DEFAULT_BALANCE_DATA)
    new_entry['_nation'] = nation
    balance_data['nations'].append(new_entry)
    print(f"Added {nation} to balance.yaml")

for nation in missing_stats_nations:
    new_entry = copy.deepcopy(DEFAULT_STATS_DATA)
    new_entry['_nation'] = nation
    stats_data['nations'].append(new_entry)
    print(f"Added {nation} to stat.yaml")

if missing_balance_nations:
    with open(balance_yaml, 'w') as f:
        yaml.safe_dump(balance_data, f, default_flow_style=False, sort_keys=False)
    print(f"Updated balance.yaml with {len(missing_balance_nations)} new nations: {', '.join(missing_balance_nations)}")
else:
    print("No new nations added to balance.yaml.")

if missing_stats_nations:
    with open(stats_yaml, 'w') as f:
        yaml.safe_dump(stats_data, f, default_flow_style=False, sort_keys=False)
    print(f"Updated stat.yaml with {len(missing_stats_nations)} new nations: {', '.join(missing_stats_nations)}")
else:
    print("No new nations added to stat.yaml.")