import requests
import xml.etree.ElementTree as ET
from datetime import date
import yaml
import os
import re
import time


def float_representer(dumper, value):
    text = f"{value:.2f}"
    return dumper.represent_scalar('tag:yaml.org,2002:float', text)

yaml.add_representer(float, float_representer)

# Import census IDs from external YAML
with open('./pcn/assets/data/census_ids.yaml', 'r') as file:
    CENSUS_IDS = yaml.safe_load(file)

def fetch_census_report(nation):
    headers = {
        'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'
    }

    census_query = '+'.join(str(id) for id in CENSUS_IDS.values())
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region+population+currency+animal+census;scale={census_query}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        new_data = {
            "Nation": nation.title(),
            "Region": root.find('REGION').text,
            "Population": int(root.find('POPULATION').text),
            "Currency": root.find('CURRENCY').text,
            "Animal": root.find('ANIMAL').text,
            "Census": {}
        }

        # Extract census data as floats
        for stat_name, census_id in CENSUS_IDS.items():
            if stat_name != "Population":
                value = float(root.find(f".//SCALE[@id='{census_id}']/SCORE").text)
                new_data["Census"][stat_name] = value 

        report_date = date.today()

        dir_path = f'./pcn/assets/data/nations/{nation}'
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = f'{dir_path}/report.yaml'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                content_no_comments = re.sub(r'#.*', '', content)
                existing_data = yaml.safe_load(content_no_comments) or {}
        else:
            existing_data = {}

        merged_data = {**existing_data, **new_data}
        yaml_content = yaml.dump(merged_data, default_flow_style=False, default_style=None)
        yaml_content += f"\n# Report generated on {report_date}\n"

        with open(file_path, 'w') as file:
            file.write(yaml_content)
        print('Retrieved report for', nation)
    else:
        print(f"Failed to fetch data for {nation}. Status code: {response.status_code}")
    time.sleep(1.5)

# Read nations and generate reports
with open('scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    fetch_census_report(nation)

print("Census Complete!")