import requests
import schedule
import time
from Stat import Stat
from HomeAssistantEntityBase import SwitchEntity
import datetime


class HomeManager:
    def __init__(self, ip, token):
        """
        Initializes the HomeManager with IP, token, and the singleton Stat instance.

        Args:
            ip (str): The IP address of the Home Assistant instance.
            token (str): The authentication token for Home Assistant.
        """
        self.ip = ip
        self.token = token
        self.stat = Stat()  # Get the singleton instance of Stat
        self.stat.add_stat("time", self.current_time)
        self.entities = []  # List to hold all entities instances
        self.selected_entities = self.load_entities()

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }

        # Fetch all entities
        response = requests.get(f"{HA_URL}/api/states", headers=headers)

        if response.status_code == 200:
            entities = response.json()
            for entity in entities:
                if entity["entity_id"] in self.selected_entities:
                    self.add_entity(entity,self.selected_entities[entity["entity_id"]])
        else:
            print(f"Failed to fetch entities: {response.status_code}, {response.text}")
    def load_entities(self):
        import json

        # Path to the JSON file
        file_path = "/Users/zvistein/Downloads/lights_logic.json"

        # Load the JSON file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    def add_entity(self, entity,logics):
        """
        Adds an entity to the HomeManager.

        Args:
            entity: The entity object (e.g., SwitchEntity) to manage.
        """
        switch_entity = SwitchEntity(entity["entity_id"], self.ip, self.token)
        for logic_item in logics['logic']:
            stat_name = logic_item['stat_name']
            value = logic_item['value']
            action = logic_item['action']
            switch_entity.logic(stat_name, value,action)

        self.entities.append(switch_entity)
        print(f"Entity added: {entity['entity_id']}")
    def run(self, interval=1):
        """
        Continuously evaluates actions at the specified interval.

        Args:
            interval (int): Time in seconds between evaluations.
        """
        print("HomeManager is running...")
        while True:
            self.stat.evaluate_actions()
            time.sleep(interval)

    # Function to get the current time
    @staticmethod
    def current_time():
        # Get the current time
        now = datetime.datetime.now().time()

        # Format the time to 'HHMM'
        formatted_time = int(f"{now.hour:02}{now.minute:02}")
        return formatted_time


if __name__ == "__main__":

    HA_URL = 'http://192.168.1.30:8123'
    TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI5MDA0ZTAxMzE1YWM0NTdkYmI4MDgxNGMxMzA3ZjY1MiIsImlhdCI6MTcxNzE2Mzg3OCwiZXhwIjoyMDMyNTIzODc4fQ.cSE3BmIlgztM-KKVaDVt119VqMU7PxSrGbmv3mBGYTs'

    manager = HomeManager(HA_URL, TOKEN)
    manager.run()

