from datetime import date
import yaml
import os
import math

balMod = 1  # Tuned down to keep bonuses in trillions, not hundreds of trillions

DEFAULT_BALANCE_DATA = {
    "FOREX": {
        "AthCoins": 0,
        "Kredits": 0
    },
    "Treasury": {
        "Sovereign": 0,
        "Trade": 0
    },
    "Portfolio": {
        "DLTA": 0
    },
    "Liabilities": {
        "001": {
            "interest": 0,
            "principal": 0,
            "creditor": "broker"
        }
    }
}

def float_representer(dumper, value):
    text = f"{value:.2f}"
    return dumper.represent_scalar('tag:yaml.org,2002:float', text)

yaml.add_representer(float, float_representer)

def load_report_data(nation):
    report_path = f'./pcn/assets/data/nations/{nation}/report.yaml'
    if not os.path.exists(report_path):
        print(f'Skipping {nation}: Report file {report_path} not found.')
        return
    with open(report_path, 'r') as file:
        report_data = yaml.safe_load(file)
    return report_data

def load_balance_data(nation):
    balance_path = f'./pcn/assets/data/nations/{nation}/balance.yaml'
    if os.path.exists(balance_path):
        with open(balance_path, 'r') as file:
            balance_data = yaml.safe_load(file)
    else:
        print(f'Creating new balance data file for {nation}.')
        balance_data = DEFAULT_BALANCE_DATA.copy()
        balance_data['Nation'] = nation.title()
        with open(balance_path, 'w') as file:
            yaml.dump(balance_data, file, default_flow_style=False)
    return balance_data

def get_balance(nation, report_data, balance_data):
    if report_data is None or balance_data is None:
        return
    
    balance_path = f'./pcn/assets/data/nations/{nation}/balance.yaml'

    # Calculate sum of industries
    industry_sum = 0
    for item in report_data['Census']['Industry']:
        industry_value = report_data['Census']['Industry'][item]
        industry_sum += max(0, industry_value)  # No negatives
    
    # Get population and economy score
    population = report_data['Population']  # NS millions, interpreted as billions
    econ = report_data['Census']['Other']['Economy']

    # Calculate quarterly deposit
    industry_output = industry_sum * population * 1_000_000
    balance_add = (industry_output * (econ / 100) * balMod) / 4

    print(f"{balance_add:,.2f} Δ to {nation}")

    # Update balance data
    balance_data['Treasury']['Sovereign'] += balance_add
    
    with open(balance_path, 'w') as file:
        yaml.dump(balance_data, file, default_flow_style=False)
    return

with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    get_balance(nation, load_report_data(nation), load_balance_data(nation))