from datetime import date
import yaml
import os



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
        "HARM": 0
    }
}

def float_representer(dumper, value):
    text = f"{value:.2f}"
    return dumper.represent_scalar('tag:yaml.org,2002:float', text)

yaml.add_representer(float, float_representer)



def load_report_data(nation):
    report_path = f'./pcn/assets/data/nations/{nation}/report.yaml'
    
    if not os.path.exists(report_path):
        print(f"Skipping {nation}: Report file {report_path} not found.")
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
        print(f"Creating new balance data file for {nation}.")
        balance_data = DEFAULT_BALANCE_DATA.copy()
        balance_data["Nation"] = nation.title()
        with open(balance_path, 'w') as file:
            yaml.dump(balance_data, file, default_flow_style=False)
    return balance_data

def get_balance(nation, report_data, balance_data):
    balance_path = f'./pcn/assets/data/nations/{nation}/balance.yaml'

    industrySum = 0

    for item in report_data["Census"]:
        if "Industry" in item:
            print(item)
            industrySum += report_data["Census"][item]

            
    
    industrySum *= report_data["Population"] * 1000000
    
    governmentSum = report_data["Census"]["Economic Output"] * 

    # NS IS FUCKED


    print(industrySum)







    
    with open(balance_path, 'w') as file:
        yaml.dump(balance_data, file, default_flow_style=False)
    return


with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    get_balance(nation, load_report_data(nation), load_balance_data(nation))