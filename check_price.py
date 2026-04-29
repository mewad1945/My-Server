import yaml
import os

# Sökvägen till din worth.yml (justera om den ligger någon annanstans)
worth_file = os.path.expanduser("~/eagler-network/smp/plugins/Essentials/worth.yml")

# Lista på items vi vill kolla (Mappade till Minecraft-IDn)
items_to_check = {
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
    "heavy_weighted_pressure_plate": "Weighted Pressure Plate (Heavy)",
    "light_weighted_pressure_plate": "Weighted Pressure Plate (Light)",
    "oak_trapdoor": "Wooden Trapdoor",
    "iron_trapdoor": "Iron Trapdoor",
    "redstone": "Redstone Dust",
    "crafter": "Auto Crafter"
}

def check_prices():
    if not os.path.exists(worth_file):
        print(f"Error: Hittade inte filen på {worth_file}")
        return

    try:
        with open(worth_file, 'r') as f:
            data = yaml.safe_load(f)
            
        # Essentials lagrar ofta priser under 'worth:'
        prices = data.get('worth', {})

        print(f"{'Item':<35} | {'Pris (worth.yml)':<15}")
        print("-" * 55)

        for internal_name, friendly_name in items_to_check.items():
            price = prices.get(internal_name, "INTE SATT")
            print(f"{friendly_name:<35} | {price:<15}")

    except Exception as e:
        print(f"Ett fel uppstod: {e}")

if __name__ == "__main__":
    check_prices()
