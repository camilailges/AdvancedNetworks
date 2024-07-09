import time
import threading
import random

class SmartWatch:
    def __init__(self, name):
        self.status = "off"
        self.name = name
        self.daily_steps = 0
        self.battery_level = 100
        self.heart_rate = 0
        self.power_saving_mode = False
        self.calories_burned = 0
        self.distance_traveled = 0.0
        self.connected_to_smartphone = False
        self.notifications = 0
        self.step_goal = 10000
        self.is_charging = False
        self.sleep_cycle = {"deep": 0, "light": 0, "rem": 0}

        self.battery_thread = threading.Thread(target=self._battery_management)
        self.battery_thread.daemon = True
        self.battery_thread.start()

    def __str__(self):
        return f"{self.name}"
    
    def set_status(self, new_status: str):
        self.status = new_status

    def update_steps(self, steps: int):
        self.daily_steps += steps

    def set_heart_rate(self, rate: int):
        self.heart_rate = rate

    def update_sleep_cycle(self):
        self.sleep_cycle["deep"] += random.randint(0, 10)
        self.sleep_cycle["light"] += random.randint(0, 10)
        self.sleep_cycle["rem"] += random.randint(0, 5)

    def update_calories_burned(self, calories: int):
        self.calories_burned += calories

    def update_distance_traveled(self, distance: float):
        self.distance_traveled += distance

    def set_connect_smartphone(self, connected: bool):
        self.connected_to_smartphone = connected

    def add_notification(self):
        self.notifications += 1

    def clear_notifications(self):
        self.notifications = 0

    def set_power_saving_mode(self, mode: bool):
        self.power_saving_mode = mode
    
    def start_charging(self):
        self.is_charging = True

    def stop_charging(self):
        self.is_charging = False

    def _battery_management(self):
        while True:
            if self.is_charging:
                if self.battery_level < 100:
                    self.battery_level += 1
                    print(f"Battery charging: {self.battery_level}%")
                time.sleep(1)
            else:
                if self.battery_level > 0:
                    if self.battery_level > 1:
                        self.battery_level -= 1
                        print(f"Battery level decreased to {self.battery_level}%")
                        time.sleep(1)

                    else:
                        self.start_charging()
            if self.battery_level == 100:
                self.stop_charging()
            time.sleep(1)