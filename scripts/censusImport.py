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

shards = 'region+population+currency+animal+sectors+tax+govt+gdp'

def fetch_census_report(nation):
    headers = {
        'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'
    }

    census_query = '+'.join(str(id) for id in CENSUS_IDS.values())
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q={shards}+census;scale={census_query}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        new_data = {
            "nation": nation.lower(),
            "region": root.find('REGION').text.lower(),
            "population": int(root.find('POPULATION').text),
            "currency": root.find('CURRENCY').text.lower(),
            "animal": root.find('ANIMAL').text.lower(),
            "gdp": int(root.find('GDP').text),
            "sectors": {
                "black market": float(root.find('SECTORS/BLACKMARKET').text),
                "government": float(root.find('SECTORS/GOVERNMENT').text),
                "industry": float(root.find('SECTORS/INDUSTRY').text),
                "public": float(root.find('SECTORS/PUBLIC').text)
            },
            "government": {
                "adm": float(root.find('GOVT/ADMINISTRATION').text),
                "def": float(root.find('GOVT/DEFENCE').text),
                "edu": float(root.find('GOVT/EDUCATION').text),
                "env": float(root.find('GOVT/ENVIRONMENT').text),
                "hea": float(root.find('GOVT/HEALTHCARE').text),
                "com": float(root.find('GOVT/COMMERCE').text),
                "aid": float(root.find('GOVT/INTERNATIONALAID').text),
                "enf": float(root.find('GOVT/LAWANDORDER').text),
                "tra": float(root.find('GOVT/PUBLICTRANSPORT').text),
                "soc": float(root.find('GOVT/SOCIALEQUALITY').text),
                "spi": float(root.find('GOVT/SPIRITUALITY').text),
                "wel": float(root.find('GOVT/WELFARE').text)
            },
            "tax": float(root.find('TAX').text),
            "census": {
                "industry": {},
                "sectors": {},
                "other": {}
            }
        }

        # Extract census data into structured subsections
        for stat_name, census_id in CENSUS_IDS.items():
            if stat_name != "population":
                value = float(root.find(f".//SCALE[@id='{census_id}']/SCORE").text)
                stat_name_lower = stat_name.lower()
                if stat_name_lower.startswith("industry: "):
                    industry_name = stat_name_lower.replace("industry: ", "")[:3]
                    new_data["census"]["industry"][industry_name] = value
                elif stat_name_lower.startswith("sector: "):
                    sector_name = stat_name_lower.replace("sector: ", "")
                    new_data["census"]["sectors"][sector_name] = value
                else:
                    new_data["census"]["other"][stat_name_lower] = value

        report_date = date.today()

        dir_path = f'./scripts/data/reports'
        os.makedirs(dir_path, exist_ok=True)
        file_path = f'{dir_path}/{nation.lower()}_report.yaml'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                content_no_comments = re.sub(r'#.*', '', content)
                existing_data = yaml.safe_load(content_no_comments) or {}
        else:
            existing_data = {}

        merged_data = {**existing_data, **new_data}
        yaml_content = yaml.dump(merged_data, default_flow_style=False, default_style=None)
        yaml_content += f"\n# report generated on {report_date}\n"

        with open(file_path, 'w') as file:
            file.write(yaml_content)
        print('Retrieved report for', nation)
    else:
        print(f"Failed to fetch data for {nation}. Status code: {response.status_code}")
    time.sleep(1.5)

# Read nations and generate reports
with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    fetch_census_report(nation)

print("Census Complete!")