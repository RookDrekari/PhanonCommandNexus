import yaml
import os

# Define industries for the template
INDUSTRIES = [
    "Automobile Manufacturing",
    "Cheese Exports",
    "Basket Weaving",
    "Information Technology",
    "Pizza Delivery",
    "Trout Fishing",
    "Arms Manufacturing",
    "Beverage Sales",
    "Timber Woodchipping",
    "Mining",
    "Insurance",
    "Furniture Restoration",
    "Retail",
    "Book Publishing",
    "Gambling"
]

# Default national data template with new structure
DEFAULT_NATIONAL_DATA = {
    "Nation": "",
    "Balances": {
        "Treasury": {
            "Sovereign": 100,
            "Trade": 100
        },
        "FOREX": {
            "Kredits": 0,
            "AthCoins": 0
        }
    },
    "Stockpiles": {
        industry: {
            f"{industry[:3].lower()}BUL": {
                "quantity": 0,
                "stockpiling": True,
                "internal_price": 0.0
            },
            f"{industry[:3].lower()}CON": {
                "quantity": 0,
                "stockpiling": True,
                "internal_price": 0.0
            },
            f"{industry[:3].lower()}LUX": {
                "quantity": 0,
                "stockpiling": True,
                "internal_price": 0.0
            }
        } for industry in INDUSTRIES
    }
}

# Load nations list
with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

def zero_out_data(nation):
    national_path = f'./data/nationalData/{nation}.yaml'
    
    # Load or create national data
    if os.path.exists(national_path):
        with open(national_path, 'r') as file:
            nation_data = yaml.safe_load(file)
    else:
        print(f"Creating new national data file for {nation}.")
        nation_data = DEFAULT_NATIONAL_DATA.copy()
        nation_data["Nation"] = nation.title()

    # Zero out Balances
    if "Balances" in nation_data:
        nation_data["Balances"]["Treasury"]["Sovereign"] = 0
        nation_data["Balances"]["Treasury"]["Trade"] = 0
        nation_data["Balances"]["FOREX"]["Kredits"] = 0
        nation_data["Balances"]["FOREX"]["AthCoins"] = 0

    # Zero out Stockpiles (only the quantity field)
    if "Stockpiles" in nation_data:
        for industry in nation_data["Stockpiles"]:
            for tier in nation_data["Stockpiles"][industry]:
                nation_data["Stockpiles"][industry][tier]["quantity"] = 0

    # Save updated national data
    with open(national_path, 'w') as file:
        yaml.dump(nation_data, file, default_flow_style=False)
        print(f"Zeroed out data for {nation}")

# Run for each nation
for nation in nations:
    zero_out_data(nation)