import yaml
import os

# Sökväg till din worth.yml
worth_file = os.path.expanduser("~/eagler-network/smp/plugins/Essentials/worth.yml")

# Lista på alla redstone-relaterade föremål du bad om
# Nyckeln är ID:t i worth.yml, värdet är ett snyggt namn för utskrift
items_to_find = {
    "daylight_detector": "Daylight Sensor",
    "dispenser": "Dispenser",
    "hopper": "Hopper",
    "dropper": "Dropper",
    "iron_door": "Iron Door",
    "jukebox": "Jukebox",
    "lever": "Lever",
    "note_block": "Note Block",
    "redstone_lamp": "Redstone Lamp",
    "redstone_torch": "Redstone Torch",
    "tripwire_hook": "Tripwire Hook",
    "comparator": "Redstone Comparator",
    "repeater": "Redstone Repeater",
    "stone_button": "Stone Button",
    "piston": "Piston",
    "sticky_piston": "Sticky Piston",
    "oak_pressure_plate": "Wooden Pressure Plate",
    "stone_pressure_plate": "Stone Pressure Plate",
    "heavy_weighted_pressure_plate": "Heavy Pressure Plate",
    "light_weighted_pressure_plate": "Light Pressure Plate",
    "oak_trapdoor": "Wooden Trapdoor",
    "iron_trapdoor": "Iron Trapdoor",
    "redstone": "Redstone Dust",
    "crafter": "Automatic Crafter"
}

def get_prices():
    if not os.path.exists(worth_file):
        print(f"Fel: Hittade inte {worth_file}")
        return

    try:
        with open(worth_file, 'r') as f:
            content = yaml.safe_load(f)
        
        # Essentials kan ha priserna direkt under 'worth' eller i roten
        prices = content.get('worth', content)

        print(f"\n{'ITEM ID':<30} | {'SÄLJPRIS (Worth)':<15}")
        print("-" * 50)

        for technical_id, display_name in items_to_find.items():
            # Vi kollar både med och utan understreck för säkerhets skull
            price = prices.get(technical_id)
            
            if price is not None:
                print(f"{technical_id:<30} | {price:<15.2f}")
            else:
                print(f"{technical_id:<30} | INTE SATT")

    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    get_prices()
