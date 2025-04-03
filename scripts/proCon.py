from datetime import date
import yaml
import os

baseODF = 0.5
decayRate = 0.95

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

# Initialize production dictionary (unchanged, integers)
industry_dict = {
    industry: {
        f"{industry[:3].lower()}BUL": 0,
        f"{industry[:3].lower()}CON": 0,
        f"{industry[:3].lower()}LUX": 0
    } for industry in INDUSTRIES
}

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
                "stockpiling": False,
                "internal_price": 0.0
            },
            f"{industry[:3].lower()}CON": {
                "quantity": 0,
                "stockpiling": False,
                "internal_price": 0.0
            },
            f"{industry[:3].lower()}LUX": {
                "quantity": 0,
                "stockpiling": False,
                "internal_price": 0.0
            }
        } for industry in INDUSTRIES
    }
}

def load_report_data(nation):
    report_path = f'./data/reports/report_{nation}.yaml'
    
    if not os.path.exists(report_path):
        print(f"Skipping {nation}: Report file {report_path} not found.")
        return

    with open(report_path, 'r') as file:
        report_data = yaml.safe_load(file)
    return report_data

def load_nation_data(nation):
    national_path = f'./data/nationalData/{nation}.yaml'
    
    if os.path.exists(national_path):
        with open(national_path, 'r') as file:
            nation_data = yaml.safe_load(file)
    else:
        print(f"Creating new national data file for {nation}.")
        nation_data = DEFAULT_NATIONAL_DATA.copy()
        nation_data["Nation"] = nation.title()
        with open(national_path, 'w') as file:
            yaml.dump(nation_data, file, default_flow_style=False)
    return nation_data

# Production
def run_production(nation, report_data, nation_data):
    # Decay stockpiles by decayRate (only if > 0)
    for industry in INDUSTRIES:
        prefix = industry[:3].lower()
        stockpiles = nation_data["Stockpiles"][industry]
        
        old_bul = stockpiles[f"{prefix}BUL"]["quantity"]
        if old_bul > 0:
            stockpiles[f"{prefix}BUL"]["quantity"] = round(old_bul * decayRate)
            print(f"{nation} {prefix}BUL stockpiles decayed by {old_bul - stockpiles[f"{prefix}BUL"]["quantity"]}")
        else:
            print(f"{nation} {prefix}BUL stockpiles <= 0, no decay applied")
        
        old_con = stockpiles[f"{prefix}CON"]["quantity"]
        if old_con > 0:
            stockpiles[f"{prefix}CON"]["quantity"] = round(old_con * decayRate)
            print(f"{nation} {prefix}CON stockpiles decayed by {old_con - stockpiles[f"{prefix}CON"]["quantity"]}")
        else:
            print(f"{nation} {prefix}CON stockpiles <= 0, no decay applied")
        
        old_lux = stockpiles[f"{prefix}LUX"]["quantity"]
        if old_lux > 0:
            stockpiles[f"{prefix}LUX"]["quantity"] = round(old_lux * decayRate)
            print(f"{nation} {prefix}LUX stockpiles decayed by {old_lux - stockpiles[f"{prefix}LUX"]["quantity"]}")
        else:
            print(f"{nation} {prefix}LUX stockpiles <= 0, no decay applied")

    # Calculate production units (skip if index <= 0)
    for industry in INDUSTRIES:
        census_key = f"Industry: {industry}"
        index = report_data["Census"][census_key]
        population = report_data["Population"] * 1000000
        
        prefix = industry[:3].lower()  # Define prefix here for each industry
        if index > 0:
            industry_dict[industry][f"{prefix}BUL"] = round(((index * population) * 0.3) / 1000000)
            industry_dict[industry][f"{prefix}CON"] = round(((index * population) * 0.6) / 10000000)
            industry_dict[industry][f"{prefix}LUX"] = round(((index * population) * 0.1) / 100000000)
            print(f"{nation} {industry} produced {industry_dict[industry][f"{prefix}BUL"]} BUL")
            print(f"{nation} {industry} produced {industry_dict[industry][f"{prefix}CON"]} CON")
            print(f"{nation} {industry} produced {industry_dict[industry][f"{prefix}LUX"]} LUX")
        else:
            industry_dict[industry][f"{prefix}BUL"] = 0
            industry_dict[industry][f"{prefix}CON"] = 0
            industry_dict[industry][f"{prefix}LUX"] = 0
            print(f"{nation} {industry} index <= 0, production skipped")

    # Add production to stockpiles
    for industry in INDUSTRIES:
        prefix = industry[:3].lower()  # Define prefix here again
        stockpiles = nation_data["Stockpiles"][industry]
        
        stockpiles[f"{prefix}BUL"]["quantity"] += industry_dict[industry][f"{prefix}BUL"]
        stockpiles[f"{prefix}CON"]["quantity"] += industry_dict[industry][f"{prefix}CON"]
        stockpiles[f"{prefix}LUX"]["quantity"] += industry_dict[industry][f"{prefix}LUX"]
        print(f"{nation} {industry} added {industry_dict[industry][f"{prefix}BUL"]} BUL to stockpile")
        print(f"{nation} {industry} added {industry_dict[industry][f"{prefix}CON"]} CON to stockpile")
        print(f"{nation} {industry} added {industry_dict[industry][f"{prefix}LUX"]} LUX to stockpile")
        
    national_path = f'./data/nationalData/{nation}.yaml'
    with open(national_path, 'w') as file:
        yaml.dump(nation_data, file, default_flow_style=False)
    print(f"Added production to {nation}")


# Industry Consumption
def run_industry_consumption(nation, report_data, nation_data):
    # Load Industry_Demand data
    with open('./data/plans/industryRules.yaml', 'r') as file:
        industry_demand = yaml.safe_load(file)["Industry_Demand"]

    # Process each industry's consumption from its inputs
    for industry in INDUSTRIES:
        prefix = industry[:3].lower()
        stockpiles = nation_data["Stockpiles"][industry]
        
        # Get production from industry_dict (set in run_production)
        total_production = (
            industry_dict[industry][f"{prefix}BUL"] +
            industry_dict[industry][f"{prefix}CON"] +
            industry_dict[industry][f"{prefix}LUX"]
        )
        total_demand = total_production * baseODF  # e.g., 50% of production
        
        # Split demand across tiers
        bul_demand = round(total_demand * 0.3)
        con_demand = round(total_demand * 0.6)
        lux_demand = round(total_demand * 0.1)
        
        # Get the demand requirements for this industry
        demand = industry_demand.get(industry, {})
        if not demand:  # Skip if no demand (e.g., Gambling: {})
            continue
        
        # For each input industry in the demand list
        for input_industry, demand_fraction in demand.items():
            input_prefix = input_industry[:3].lower()
            input_stockpiles = nation_data["Stockpiles"][input_industry]
            
            # Calculate consumption based on demand fraction
            bul_consumed = round(bul_demand * demand_fraction)
            con_consumed = round(con_demand * demand_fraction)
            lux_consumed = round(lux_demand * demand_fraction)
            
            # Subtract from input industry's stockpiles
            input_stockpiles[f"{input_prefix}BUL"]["quantity"] -= bul_consumed
            input_stockpiles[f"{input_prefix}CON"]["quantity"] -= con_consumed
            input_stockpiles[f"{input_prefix}LUX"]["quantity"] -= lux_consumed
            
            # Log the withdrawals
            print(f"{nation} {industry} withdrew {bul_consumed} BUL from {input_industry}")
            print(f"{nation} {industry} withdrew {con_consumed} CON from {input_industry}")
            print(f"{nation} {industry} withdrew {lux_consumed} LUX from {input_industry}")

    # Save updated national data
    national_path = f'./data/nationalData/{nation}.yaml'
    with open(national_path, 'w') as file:
        yaml.dump(nation_data, file, default_flow_style=False)
    print(f"Withdrew industry consumption from {nation}")


def run_consumer_consumption(nation, report_data, nation_data):
    return

def run_government_consumption(nation, report_data, nation_data):
    return

# Load nations list
with open('./scripts/nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

for nation in nations:
    run_production(nation, load_report_data(nation), load_nation_data(nation))
    run_industry_consumption(nation, load_report_data(nation), load_nation_data(nation))
    run_consumer_consumption(nation, load_report_data(nation), load_nation_data(nation))
    run_government_consumption(nation, load_report_data(nation), load_nation_data(nation))