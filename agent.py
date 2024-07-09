#!/usr/bin/env python3

import sys
import json

# Path to the JSON file with the SmartWatch data
json_file_path = '/workspaces/AdvancedNetworks/smartwatch_data.json'

def load_data():
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print("Failed to load JSON data:", e)
        sys.exit(1)

# Load the SmartWatch data at the start of the script
smartwatch_data = load_data()



def save_data():
    try:
        with open(json_file_path, 'w') as file:
            json.dump(smartwatch_data, file, indent=4)
        return "Data saved successfully"
    except Exception as e:
        return f"Failed to save JSON data: {e}"

def get_oid_value(oid):
    mappings = {
        ".1.3.6.1.3.1234.1.1.0": ("string", smartwatch_data["status"]),
        ".1.3.6.1.3.1234.1.2.0": ("string", smartwatch_data["name"]),
        ".1.3.6.1.3.1234.1.3.0": ("integer", smartwatch_data["daily_steps"]),
        ".1.3.6.1.3.1234.1.4.0": ("integer", smartwatch_data["battery_level"]),
        ".1.3.6.1.3.1234.1.5.0": ("integer", smartwatch_data["heart_rate"]),
        ".1.3.6.1.3.1234.1.6.0": ("integer", int(smartwatch_data["power_saving_mode"])),
        ".1.3.6.1.3.1234.1.7.0": ("integer", smartwatch_data["calories_burned"]),
        ".1.3.6.1.3.1234.1.8.0": ("integer", smartwatch_data["distance_traveled"]),
        ".1.3.6.1.3.1234.1.9.0": ("integer", int(smartwatch_data["connected_to_smartphone"])),
        ".1.3.6.1.3.1234.1.10.0": ("integer", smartwatch_data["notifications"]),
        ".1.3.6.1.3.1234.1.11.0": ("integer", smartwatch_data["step_goal"]),
        ".1.3.6.1.3.1234.1.12.0": ("integer", int(smartwatch_data["is_charging"])),
        ".1.3.6.1.3.1234.1.13.1": ("integer", smartwatch_data["sleep_cycle"]["deep"]),
        ".1.3.6.1.3.1234.1.13.2": ("integer", smartwatch_data["sleep_cycle"]["light"]),
        ".1.3.6.1.3.1234.1.13.3": ("integer", smartwatch_data["sleep_cycle"]["rem"])
    }
    return mappings if oid is None else mappings.get(oid, (None, None))


def handle_get(oid):
    result = get_oid_value(oid)
    if result[0] is not None:
        return f"{oid}\n{result[0]}\n{result[1]}"
    return "NONE"

def handle_getnext(oid):
    oids = sorted(get_oid_value(None).keys())
    next_oid_index = oids.index(oid) + 1 if oid in oids else 0
    if next_oid_index < len(oids):
        return handle_get(oids[next_oid_index])
    return "NONE"

def handle_set(oid, type, value):
    oid_key = oid.split('.')[-1]
    writable_oids = {
        ".1.3.6.1.3.1234.1.2.0": "name",  # name (read-write)
        ".1.3.6.1.3.1234.1.6.0": "power_saving_mode",  # power_saving_mode (read-write, boolean)
        ".1.3.6.1.3.1234.1.11.0": "step_goal",  # step_goal (read-write)
    }
    if oid in writable_oids:
        if type == "integer":
            smartwatch_data[writable_oids[oid]] = int(value)
        elif type == "string":
            smartwatch_data[writable_oids[oid]] = value
        else:
            return "Unsupported type for SET"
        save_data()
        return f"SET SUCCESS: {oid} set to {value}"
    return "SET FAILURE: OID not writable or does not exist"

def main():
    if len(sys.argv) < 3:
        print("Usage: agent.py -g|-n|-s OID [type] [new_value]")
        return

    request_type = sys.argv[1]
    oid = sys.argv[2]

    if request_type == "-g":  # GET request
        print(handle_get(oid))
    elif request_type == "-n":  # GETNEXT request
        print(handle_getnext(oid))
    elif request_type == "-s" and len(sys.argv) == 5:  # SET request
        type = sys.argv[3]
        new_value = sys.argv[4]
        print(handle_set(oid, type, new_value))
    else:
        print("NONE")

if __name__ == "__main__":
    main()


# python3 agent.py -s 1.3.6.1.3.1234.1.11.0 integer 15000
