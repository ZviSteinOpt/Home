import requests
from Stat import Stat

class HomeAssistantEntity:
    def __init__(self, entity_id, ha_url, token):
        self.entity_id = entity_id
        self.ha_url = ha_url
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',  # Token used for authenticating API requests
            'content-type': 'application/json',  # Ensures the request payload is sent as JSON
        }

    def call_service(self, domain, service, data=None):
        """
        Makes an HTTP POST request to call a specific Home Assistant service.

        Args:
            domain (str): The domain of the service (e.g., 'switch', 'light', 'cover').
            service (str): The specific service to call (e.g., 'turn_on', 'turn_off', 'set_cover_position').
            data (dict, optional): Additional data required for the service, such as parameters.

        Example:
            To turn on a switch:
            domain = 'switch', service = 'turn_on'

            To set a cover position:
            domain = 'cover', service = 'set_cover_position', data = {'position': 50}
        """
        # Build the URL for the Home Assistant API endpoint
        url = f'{self.ha_url}/api/services/{domain}/{service}'

        # Prepare the payload with the entity ID and additional data if provided
        payload = {'entity_id': self.entity_id}
        if data:
            payload.update(data)  # Merge additional data into the payload

        # Send the HTTP POST request
        response = requests.post(url, headers=self.headers, json=payload)

        # Check the response status
        if response.status_code == 200:
            # The service call was successful
            print(f'Successfully called service {service} on {self.entity_id}')
        else:
            # The service call failed, log the error
            print(f'Failed to call service {service} on {self.entity_id}: {response.content}')


class SwitchEntity(HomeAssistantEntity):
    def __init__(self, entity_id, ha_url, token):
        super().__init__(entity_id, ha_url, token)
        self.operation_log = []  # Store all function calls for tracking
        self.stats = Stat()  # Get the singleton instance of Stat

        # Map of action strings to methods
        self.action_map = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
        }

    def turn_on(self):
        self.call_service('switch', 'turn_on')
        print(f"Switch {self.entity_id} turned on.")
        self.operation_log.append(('turn_on', self.entity_id))

    def turn_off(self):
        self.call_service('switch', 'turn_off')
        print(f"Switch {self.entity_id} turned off.")
        self.operation_log.append(('turn_off', self.entity_id))

    def logic(self, stat_name, value, action):
        """
        Assigns an action for a stat.

        Args:
            stat_name (str): The name of the stat to check.
            value (any): The value the stat should match to trigger the action.
            action (str): The name of the action to execute if the value matches.
                          Must match a key in `self.action_map`.
        """
        if action not in self.action_map:
            raise ValueError(f"Action '{action}' is not valid. Valid actions: {list(self.action_map.keys())}")

        # Assign the corresponding function from action_map to the stat
        self.stats.assign_action(stat_name, condition=value, action=self.action_map[action])