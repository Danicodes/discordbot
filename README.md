# Making a Discord bot

The purpose of this is to show a range of example applications for a bot; because the repo utilizes discord.py, translating this to another communication platform may not be 1:1   

## Setup
1. To register a new bot application go to [discord's developer portal](discord.com/developers/applications)
2. Set up your bot with the necessary permissions for the application you're making
3. Generate an invite link which will allow you (the user) to select which server to invite your bot to

## Organization
The code is organized into a main entry point (bot.py) which connects to the discord client as the bot user and 
cogs which allow us to hot-reload modular portions of code into the application.

## Cogs
The cogs I've included are intended to mock a range of scenarios in which we could find ourselves utilizing a chatbot
### 1. admin
Contains functions that allow us to hot-reload cogs within the discord client! This gets loaded when the bot starts.
### 2. general
Used to test a basic cog load with a couple of simple commands
### 3. productive
Mock scenario of creating an incident channel, and monitoring an event related to the incident in the discord client
### 4. sentience
Serves to demonstrate using an AI/ML model as a utility
### 5. decisions
A mock customer service decision tree, made to 'help' with an order. Uses json data in place of using a database connection to store and retrieve data
### 6. safety
Example of creating safety tools for a server - includes the ability to purge messages, add blacklisted terms, timeout users
### 7. welcome
Mostly included this to show an example of adding and reading reactions (this can be useful to trigger an action based on a reaction to a message)
### 8. voice
This one I just did for fun

## Resources
### Discord
Link to the [Discord API](https://discord.com/developers/docs/intro)

Link to documentation for the discord api wrapper in python [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html)

### Slack
If you're using slack as a communication tool, [here](https://api.slack.com/web) are some api documentation that may help you achieve similar functionality

[Python slack sdk](https://slack.dev/python-slack-sdk/)
