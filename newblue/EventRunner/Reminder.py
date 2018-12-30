import Event

class Reminder(event):
    def __init__(self, name, repeating, repeat_interval=None):
        super().__init__(name, repeating, repeat_interval)
        self.load_config()

    def load_config(self):
        with open('opts.json') as file:
            data = json.loads(file)
            self.channel_id = data[self.name]['channel_id']
            self.role_ids = data[self.name]['role_ids']