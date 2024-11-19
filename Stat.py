class Stat:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Stat, cls).__new__(cls, *args, **kwargs)
            cls._instance.stats = {}  # Dictionary to hold stats and their value functions
            cls._instance.actions = {}  # Dictionary to hold assigned actions
        return cls._instance

    def add_stat(self, stat_name, value_function):
        """
        Adds or updates a stat with the given name and a function to provide its value.

        Args:
            stat_name (str): The name of the stat (e.g., 'time', 'temperature').
            value_function (callable): A function that returns the current value of the stat.
        """
        if not callable(value_function):
            raise ValueError("value_function must be a callable function.")
        self.stats[stat_name] = value_function
        print(f"Stat added: {stat_name}")

    def assign_action(self, stat_name, condition, action):
        """
        Assigns an action to be executed when a stat's value matches the condition.

        Args:
            stat_name (str): The name of the stat to monitor.
            condition (any): The value that the stat's current value should match.
            action (callable): A function to execute when the condition is met.
        """
        if not callable(action):
            raise ValueError("Action must be a callable function.")
        if stat_name not in self.stats:
            raise ValueError(f"Stat {stat_name} must be added before assigning an action.")
        self.actions[stat_name] = (condition, action)
        print(f"Action assigned to stat: {stat_name}, Condition: {condition}")

    def evaluate_actions(self):
        """
        Evaluates all assigned actions and executes them if their conditions are met.
        """
        for stat_name, (condition, action) in self.actions.items():
            if stat_name in self.stats:
                value = self.stats[stat_name]()  # Get the current value of the stat
                if value == condition:
                    print(f"Condition met for {stat_name}: {value} == {condition}. Executing action.")
                    action()
                else:
                    print(f"Condition not met for {stat_name}: {value} != {condition}.")