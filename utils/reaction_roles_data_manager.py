import json


class ReactionRolesDataManager:

    # The instance of the ReactionRolesDataManager class
    instance = None

    @staticmethod
    def get_instance():
        """
        Gets the instance of the ReactionRolesDataManager
        :return instance:
        """
        if ReactionRolesDataManager.instance is None:
            ReactionRolesDataManager.instance = ReactionRolesDataManager()

        return ReactionRolesDataManager.instance

    @staticmethod
    def create_instance():
        """
        Creates the instance of ReactionRolesDataManager
        """
        ReactionRolesDataManager.instance = ReactionRolesDataManager()

    @staticmethod
    def reload():
        """
        Creates a new instance of the manager with the data saved in JSON
        """
        ReactionRolesDataManager.instance = ReactionRolesDataManager()

    def __init__(self):
        self.reaction_messages = []
        self.reaction_roles = {}
        self.load_json_data()
        ReactionRolesDataManager.instance = self

    def load_json_data(self):
        """
        Loads the reaction role data from reaction_roles.json
        Assigns data to class instance variables
        """
        with open("reaction_roles.json", "r") as f:
            file = json.load(f)

        self.reaction_messages = [int(i) for i in file.keys()]

        for message in self.reaction_messages:
            self.reaction_roles[message] = file[str(message)]

    def get_role_id(self, message_id, emoji):
        """
        Gets the role_id for the reaction role for the given message with the given emoji
        :param message_id: The int message id
        :param emoji: The string name of the emoji
        :return:
        """
        try:
            reaction = (self.reaction_roles[message_id])[emoji]
        except KeyError:
            return None
        return reaction["role_id"]

    def add_reaction_role(self, message_id, emoji_name, role_id):
        """
        Adds the reaction role for the given message for the given emoji.
        Updates active reaction_roles and saves to json
        :param message_id: The id of the message
        :param emoji_name: The string name of the emoji
        :param role_id: The numerical id of the role
        :return:
        """
        if int(message_id) not in self.reaction_messages:
            self.reaction_messages.append(int(message_id))
            self.reaction_roles[int(message_id)] = {}

        reaction_role = self.reaction_roles.get(int(message_id))
        reaction_role[emoji_name] = {"role_id": int(role_id)}

        with open("reaction_roles.json", "w") as f:
            json.dump(self.reaction_roles, f, indent=4)

    def remove_reaction_role(self, message_id, emoji_name):
        """
        Removes the given reaction role from the given message
        :param message_id: The snowflake id of the message
        :param emoji_name: The string name of the emoji
        """

        if len(self.reaction_roles.get(int(message_id)).keys()) <= 1:
            self.reaction_messages.remove(message_id)

        reaction_role = self.reaction_roles.get(int(message_id))
        reaction_role.pop(str(emoji_name))
        self.reaction_roles[int(message_id)] = reaction_role

        # Saves the changes to the JSON file
        with open("reaction_roles.json", "w") as f:
            json.dump(self.reaction_roles, f, indent=4)

    def clear_reaction_roles(self, message_id):
        """
        Removes the given reaction role from the given message
        :param message_id: The snowflake id of the message
        """

        if int(message_id) in self.reaction_messages:
            self.reaction_messages.remove(int(message_id))

        self.reaction_roles.pop(int(message_id))

        # Saves the changes to the JSON file
        with open("reaction_roles.json", "w") as f:
            json.dump(self.reaction_roles, f, indent=4)
