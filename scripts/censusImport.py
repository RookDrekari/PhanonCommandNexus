import requests
import xml.etree.ElementTree as ET
from datetime import date
import yaml
import os
import re

# Complete census IDs from your list
CENSUS_IDS = {
    "Civil Rights": 0,
    "Economy": 1,
    "Political Freedoms": 2,
    "Population": 3,  # Handled separately via POPULATION tag
    "Wealth Gaps": 4,
    "Death Rate": 5,
    "Compassion": 6,
    "Eco-Friendliness": 7,
    "Social Conservatism": 8,
    "Nudity": 9,
    "Industry: Automobile Manufacturing": 10,
    "Industry: Cheese Exports": 11,
    "Industry: Basket Weaving": 12,
    "Industry: Information Technology": 13,
    "Industry: Pizza Delivery": 14,
    "Industry: Trout Fishing": 15,
    "Industry: Arms Manufacturing": 16,
    "Sector: Agriculture": 17,
    "Industry: Beverage Sales": 18,
    "Industry: Timber Woodchipping": 19,
    "Industry: Mining": 20,
    "Industry: Insurance": 21,
    "Industry: Furniture Restoration": 22,
    "Industry: Retail": 23,
    "Industry: Book Publishing": 24,
    "Industry: Gambling": 25,
    "Sector: Manufacturing": 26,
    "Government Size": 27,
    "Welfare": 28,
    "Public Healthcare": 29,
    "Law Enforcement": 30,
    "Business Subsidization": 31,
    "Religiousness": 32,
    "Income Equality": 33,
    "Niceness": 34,
    "Rudeness": 35,
    "Intelligence": 36,
    "Ignorance": 37,
    "Political Apathy": 38,
    "Health": 39,
    "Cheerfulness": 40,
    "Weather": 41,
    "Compliance": 42,
    "Safety": 43,
    "Lifespan": 44,
    "Ideological Radicality": 45,
    "Defense Forces": 46,
    "Pacifism": 47,
    "Economic Freedom": 48,
    "Taxation": 49,
    "Freedom From Taxation": 50,
    "Corruption": 51,
    "Integrity": 52,
    "Authoritarianism": 53,
    "Youth Rebelliousness": 54,
    "Culture": 55,
    "Employment": 56,
    "Public Transport": 57,
    "Tourism": 58,
    "Weaponization": 59,
    "Recreational Drug Use": 60,
    "Obesity": 61,
    "Secularism": 62,
    "Environmental Beauty": 63,
    "Charmlessness": 64,
    "Influence": 65,
    "World Assembly Endorsements": 66,
    "Averageness": 67,
    "Human Development Index": 68,
    "Primitiveness": 69,
    "Scientific Advancement": 70,
    "Inclusiveness": 71,
    "Average Income": 72,
    "Average Income of Poor": 73,
    "Average Income of Rich": 74,
    "Public Education": 75,
    "Economic Output": 76,
    "Crime": 77,
    "Foreign Aid": 78,
    "Black Market": 79,
    "Residency": 80,
    "Survivors": 81,
    "Zombies": 82,
    "Dead": 83,
    "Percentage Zombies": 84,
    "Average Disposable Income": 85,
    "International Artwork": 86,
    "Patriotism": 87,
    "Food Quality": 88
}

def fetch_census_report(nation):
    headers = {
        'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'
    }

    # Query all census IDs
    census_query = '+'.join(str(id) for id in CENSUS_IDS.values())
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region+population+currency+animal+census;scale={census_query}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        new_data = {
            "Nation": nation.title(),
            "Region": root.find('REGION').text,
            "Population": int(root.find('POPULATION').text),  # In millions, per NS API
            "Currency": root.find('CURRENCY').text,
            "Animal": root.find('ANIMAL').text,
            "Census": {}
        }

        # Extract all census data
        for stat_name, census_id in CENSUS_IDS.items():
            if stat_name != "Population":  # Population handled separately
                value = float(root.find(f".//SCALE[@id='{census_id}']/SCORE").text)
                new_data["Census"][stat_name] = value

        # Add report date
        report_date = date.today()

        # Load existing data, strip comments
        file_path = f'./data/reports/report_{nation}.yaml'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                content_no_comments = re.sub(r'#.*', '', content)
                existing_data = yaml.safe_load(content_no_comments) or {}
        else:
            existing_data = {}

        # Merge and save
        merged_data = {**existing_data, **new_data}
        yaml_content = yaml.dump(merged_data, default_flow_style=False)
        yaml_content += f"\n# Report generated on {report_date}\n"

        with open(file_path, 'w') as file:
            file.write(yaml_content)
        print('Retrieved report for', nation)
    else:
        print(f"Failed to fetch data for {nation}. Status code: {response.status_code}")

# Read nations from file and generate reports
with open('scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    fetch_census_report(nation)