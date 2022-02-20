import discord
import toml

from bot.duck_bot import DuckBot


def load_config_data():
    """ Loads all config data from the duck_bot_config.toml file. """
    return toml.load("duck_bot_config.toml")


if __name__ == "__main__":
    # Loads the config and gets all needed values
    config = load_config_data()
    cogs = config.get("DuckBot").get("cogs")
    token = config.get("DuckBot").get("token")
    prefix = config.get("DuckBot").get("prefix")

    # Assigns the discord intents needed for the bot
    intents = discord.Intents.default()
    intents.members = True

    # Creates and runs the instance of the DuckBot class
    bot = DuckBot(command_prefix=prefix, intents=intents, available_cogs=cogs, bot_config=config)
    bot.run(token)

