import telebot
import brawlstats
from telebot import types

# Tokens
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
brawlstars_token = 'YOUR_BRAWLSTARS_API_TOKEN'

# Clients
client = brawlstats.Client(brawlstars_token)
bot = telebot.TeleBot(telegram_token)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📊 Send Tag"))
    bot.send_message(
        message.chat.id,
        "Hey there! 👋\nI'm your Brawl Stars stats bot.\n\n"
        "Just send me your player tag (e.g. `#ABCD1234`) and I'll show you your profile!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Main message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if text.startswith("#") and len(text) > 4:
        player_tag = text[1:].upper()

        try:
            player = client.get_player(player_tag)
            response = (
                f"🔥 *Name:* {player.name}\n"
                f"🆔 *Tag:* `#{player.tag}`\n"
                f"🏆 *Trophies:* {player.trophies}\n"
                f"🥇 *Best Trophies:* {player.highest_trophies}\n"
                f"🎯 *Level:* {player.exp_level}\n\n"
                f"📊 *Battle Stats:*\n"
                f"• 🥷 3v3 Victories: `{player['3vs3_victories']}`\n"
                f"• ⚔️ Solo Showdown Wins: `{player.solo_victories}`\n"
                f"• 🤝 Duo Showdown Wins: `{player.duo_victories}`\n"
                f"• 🧩 Total Victories: `{player.total_victories}`\n"
                f"• 🧠 Highest Robo Rumble Level: `{player.best_robo_rumble_time}`\n"
                f"• 🚀 Highest Boss Fight Level: `{player.best_time_as_big_brawler}`"
            )
            bot.reply_to(message, response, parse_mode="Markdown")
        except brawlstats.NotFoundError:
            bot.reply_to(message, "❌ No player found with this tag. Please check if it's correct.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: `{str(e)}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send a valid player tag starting with `#` (e.g. `#ABCD1234`)", parse_mode="Markdown")

# Run the bot
bot.polling()

