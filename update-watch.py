import threading
import random
import time
import json
from SmartWatch import SmartWatch

def update_watch(smartwatch):
    smartwatch.set_status("on")
    while True:
        smartwatch.set_heart_rate(random.randint(60, 100))
        smartwatch.update_calories_burned(random.randint(0, 50))
        smartwatch.add_notification()
        
        if random.choice([True, False]):
            smartwatch.set_connect_smartphone(True)
        else:
            smartwatch.set_connect_smartphone(False)

        if random.choice([True, False]):
            smartwatch.set_power_saving_mode(True)
        else:
            smartwatch.set_power_saving_mode(False)

        if random.random() <= 0.1:
            smartwatch.set_status("sleep")
        else:
            smartwatch.set_status("on")

        if smartwatch.status == "sleep":
            smartwatch.update_sleep_cycle()
        else:
          smartwatch.update_distance_traveled(random.uniform(0.0, 0.1))
          smartwatch.update_steps(random.randint(0, 100))

        time.sleep(10)

def main():
    smartwatch = SmartWatch("MySmartWatch")
    
    update_thread = threading.Thread(target=update_watch, args=(smartwatch,))
    update_thread.daemon = True
    update_thread.start()
    
    while True:
        watch_data = {
            "status": smartwatch.status,
            "name": smartwatch.name,
            "daily_steps": smartwatch.daily_steps,
            "battery_level": smartwatch.battery_level,
            "heart_rate": smartwatch.heart_rate,
            "power_saving_mode": smartwatch.power_saving_mode,
            "sleep_cycle": smartwatch.sleep_cycle,
            "calories_burned": smartwatch.calories_burned,
            "distance_traveled": smartwatch.distance_traveled,
            "connected_to_smartphone": smartwatch.connected_to_smartphone,
            "notifications": smartwatch.notifications,
            "step_goal": smartwatch.step_goal,
            "is_charging": smartwatch.is_charging,
        }
        
        with open("smartwatch_data.json", "w") as json_file:
            json.dump(watch_data, json_file, indent=4)
        
        time.sleep(10)

if __name__ == "__main__":
  main()