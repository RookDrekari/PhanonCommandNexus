from datetime import date
import yaml
import os
import math

delta = 1000000000

def float_representer(dumper, value):
    text = f"{value:.2f}"
    return dumper.represent_scalar('tag:yaml.org,2002:float', text)

yaml.add_representer(float, float_representer)

def load_report_data(nation):
    report_path = f'./scripts/data/reports/{nation}_REPORT.yaml'
    
    if not os.path.exists(report_path):
        print(f'Skipping {nation}: Report file {report_path} not found.')
        return None

    with open(report_path, 'r') as file:
        return yaml.safe_load(file)

def load_stats_data():
    stats_yaml = './scripts/data/stats.yaml'

    try:
        with open(stats_yaml, 'r') as f:
            return yaml.safe_load(f) or {'nations': []}
    except FileNotFoundError:
        print(f"Error: {stats_yaml} not found.")
        return {'nations': []}

def save_stats_data(stats_data):
    stats_yaml_file = './scripts/data/stats.yaml'
    with open(stats_yaml_file, 'w') as file:
        yaml.safe_dump(stats_data, file, default_flow_style=False)

def get_stats(nation, report_data, stats_data):
    if report_data is None:
        return

    for nation_stats in stats_data['nations']:
        if nation_stats['_nation'] == nation:
            print(f"Processing {nation}")
            calcSum = 0
            nation_stats['econ']['government']['sum'] = 0
            nation_stats['econ']['business']['sum'] = 0
            nation_stats['econ']['population'] = report_data['population'] * 1000000
            nation_stats['econ']['production'] = round(report_data['gdp'] / delta, 2)
            nation_stats['econ']['government']['sum'] = round( nation_stats['econ']['production'] * ( .01 * report_data['sectors']['government'] ), 2 )
            nation_stats['econ']['illegal'] = round( nation_stats['econ']['production'] * ( .01 * report_data['sectors']['black market'] ), 2)
            nation_stats['econ']['private'] = round( nation_stats['econ']['production'] * ( .01 * report_data['sectors']['industry'] ), 2)
            nation_stats['econ']['public'] = round( nation_stats['econ']['production'] * ( .01 * report_data['sectors']['public'] ), 2)      
            for business in nation_stats['econ']['business']:
                if business != 'sum':
                    nation_stats['econ']['business'][business] = max(round(( report_data['census']['industry'][business] * nation_stats['econ']['population'] ) / delta, 2), 0)
                    calcSum += nation_stats['econ']['business'][business]
                nation_stats['econ']['business']['sum'] = round(calcSum, 2)    
            for govern in nation_stats['econ']['government']:
                if govern != 'sum':
                    nation_stats['econ']['government'][govern] = max(round(( report_data['government'][govern] * nation_stats['econ']['population'] ) / delta, 2), 0)
            nation_stats['econ']['business']['sum'] = round(calcSum, 2)
            return nation_stats

    print(f"Error: {nation} not found in stats.yaml.")

with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file if line.strip()]

stats_data = load_stats_data()
for nation in nations:
    get_stats(nation, load_report_data(nation), stats_data)

save_stats_data(stats_data)
print("Updated stats.yaml with all changes.")