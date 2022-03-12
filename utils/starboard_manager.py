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
        self.messages = self.load_starboard_messages()

    def load_starboard_messages(self):
        """ Loads the list of starboard message ids """

        try:
            with open("starboard_messages.json", "r") as f:
                file = json.load(f)

        except FileNotFoundError:
            file = []
            with open("starboard_messages.json", "w") as f:
                json.dump(file, f)

        return file

    def add_message(self, new_message_id):
        """ Adds a message to the starboard message list """

        self.messages.append(new_message_id)

        with open("starboard_messages.json", "w") as f:
            json.dump(self.messages, f, indent=4)

