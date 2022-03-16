import json


class StarboardManager:

    # The instance of the StarboardManager
    instance = None

    @staticmethod
    def get_instance():
        """
        Gets the instance of the ReactionRolesDataManager
        :return instance:
        """

        return StarboardManager.instance

    def __init__(self, starboard_toml):

        StarboardManager.instance = self
        self.emoji = starboard_toml.get("starboardEmoji")
        self.reaction_threshold = starboard_toml.get("reactionThreshold")
        self.channel_id = starboard_toml.get("starboardChannelId")
        self.messages = []
        self.messages_dict = {}
        self.load_starboard_messages()

    def load_starboard_messages(self):
        """ Loads the list of starboard message ids """

        try:
            with open("starboard_messages.json", "r") as f:
                file = json.load(f)

            if type(file) == list:
                file = {}
                with open("starboard_messages.json", "w") as f:
                    json.dump(file, f)

        except FileNotFoundError:
            file = {}
            with open("starboard_messages.json", "w") as f:
                json.dump(file, f)

        self.messages = [int(i) for i in file.keys()]
        self.messages_dict = file

    def add_message(self, new_message_id, starboard_message_id):
        """ Adds a message to the starboard message list """

        self.messages.append(new_message_id)
        self.messages_dict[str(new_message_id)] = starboard_message_id

        with open("starboard_messages.json", "w") as f:
            json.dump(self.messages_dict, f, indent=4)

    def get_starboard_message_id(self, message_id):
        """ Gets the Id of the starboard message """

        if message_id in self.messages:

            return self.messages_dict[str(message_id)]

    def remove_message(self, message_id):
        """ Removes a message from the starboard """

        self.messages.remove(message_id)
        self.messages_dict.pop(str(message_id))

        with open("starboard_messages.json", "w") as f:
            json.dump(self.messages_dict, f, indent=4)

    def delete_message(self, message_id):
        """ Deletes the starboard message from the database and returns the ID of the starboard message """

        starboard_message_id = self.get_starboard_message_id(message_id)
        self.remove_message(message_id)

        return starboard_message_id

