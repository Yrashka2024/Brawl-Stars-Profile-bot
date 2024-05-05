import telebot
import brawlstats

# Specify the token of your Telegram bot
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
# Specify the Brawl Stars API token (available on the website https://developer.brawlstars.com )
brawlstars_token = 'YOUR_BRAWLSTARS_API_TOKEN'

# Creating a client object Brawl Stars
client = brawlstats.Client(brawlstats_token)
# Creating a bot object
bot = telebot.TeleBot(telegram_token)

# Command handler /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! To find out the statistics of your Brawl Stars profile, submit your game tag.")

# Text message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
# We receive the text of the message from the user
    text = message.text.strip()
# Check if the text of the message is a player tag
    if text.startswith("#"):
# Extract the player tag
        player_tag = text[1:]
        try:
            # We get the player's profile data by his tag
            player = client.get_player(player_tag)
            # We form a reply message with the player's profile data
            response = f"Player name: {player.name }\Tag: #{player.tag}\Trophies: {player.trophies}\Best trophy: {player.highest_trophies}\Level: {player.exp_level}"
# Sending a reply message to the user
            bot.reply_to(message, response)
        except brawlstats.NotFoundError:
            # In case of an error, we send an error message
            bot.reply_to(message, "No player with this tag was found.")
except Exception as e:
            # In case of other errors, we send an error message
            bot.reply_to(message, f"Error: {str(e)}")
else:
# If the message does not contain a player tag, we send a hint
        bot.reply_to(message, "To find out the statistics of your Brawl Stars profile, send your game tag starting with #.")

# Launching the bot
bot.polling()
