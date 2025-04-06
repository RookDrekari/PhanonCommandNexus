import yaml
import os

COMMODITIES_FILE = os.path.join(os.path.dirname(__file__), 'commodities.yaml')
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'new_products.yaml')

def load_commodities():
    if os.path.exists(COMMODITIES_FILE):
        with open(COMMODITIES_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    return {}

def save_commodities(data):
    with open(COMMODITIES_FILE, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    print(f"Updated commodities saved to {COMMODITIES_FILE}")

def import_products():
    commodities = load_commodities()

    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please create it with new products.")
        return

    try:
        with open(INPUT_FILE, 'r') as file:
            new_products = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Error parsing {INPUT_FILE}: {e}")
        print("Expected format:")
        print('  Product:')
        print('    Name: "Example"')
        print('    Category: "XXXBUL"')
        print('    Description: "Example description"')
        print('    Global: true')
        print('    Origin: "Commodities Broker"')
        return

    if not new_products:
        print(f"Error: {INPUT_FILE} is empty.")
        return

    products_list = new_products if isinstance(new_products, list) else [new_products]

    for product_entry in products_list:
        if 'Product' not in product_entry:
            print("Error: Missing 'Product' key. Skipping.")
            continue

        product_data = product_entry['Product']
        product_name = product_data.get('Name')
        if not product_name:
            print("Error: Missing 'Name' in 'Product'. Skipping.")
            continue

        category = product_data.get('Category', '').upper()
        description = product_data.get('Description', 'No description provided')
        global_flag = product_data.get('Global', True)
        origin = product_data.get('Origin', 'Commodities Broker')  # Default origin

        cb_import = 0.75
        cb_export = 1.25

        industry_prefix = category[:3]
        industry_map = {
            'ARM': 'Arms Manufacturing', 'AUT': 'Automobile Manufacturing',
            'BAS': 'Basket Weaving', 'BEV': 'Beverage Sales', 'BOO': 'Book Publishing',
            'CHE': 'Cheese Exports', 'FUR': 'Furniture Restoration', 'GAM': 'Gambling',
            'INF': 'Information Technology', 'INS': 'Insurance', 'MIN': 'Mining',
            'PIZ': 'Pizza Delivery', 'RET': 'Retail', 'TIM': 'Timber Woodchipping',
            'TRO': 'Trout Fishing'
        }
        industry = industry_map.get(industry_prefix)
        if not industry:
            print(f"Error: Invalid category prefix in {category}. Skipping.")
            continue

        if industry not in commodities:
            commodities[industry] = {}

        if category not in commodities[industry]:
            commodities[industry][category] = {}

        if product_name in commodities[industry][category]:
            print(f"Warning: {product_name} already exists in {industry}/{category}. Skipping.")
            continue

        commodities[industry][category][product_name] = {
            'cbImport': cb_import,
            'cbExport': cb_export,
            'Global': global_flag,
            'desc': description,
            'Origin': origin
        }
        print(f"Added {product_name} to {industry}/{category}")

    save_commodities(commodities)

if __name__ == "__main__":
    import_products()