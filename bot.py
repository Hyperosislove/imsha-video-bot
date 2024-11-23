import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Fetch sensitive info from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Initialize bot client
bot = Client("video_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to create inline keyboard with buttons
def create_keyboard():
    buttons = [
        [InlineKeyboardButton("PART1 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART2 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART3 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART4 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART5 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART6 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")],
        [InlineKeyboardButton("PART7 🔞", url="https://t.me/PAWSOG_bot/PAWS?startapp=2CCfBLTA")]
    ]
    return InlineKeyboardMarkup(buttons)

@bot.on_message(filters.command("start"))
async def start(client, message):
    text = (
        "🌟 **Imsha Rehman** 🌟\n\n"
        "❤️ **Full video available!** Click on the button below to watch the complete video. All parts are just a tap away! 😘🔥🔥🥵🫦🍑\n\n"
        "👇👇👇👇👇👇👇👇👇👇\n\n"
        "**عِمشہ رحمان** ke tamam parts dekhne ke liye neeche diye gaye button par click karein. 💖✨\n\n"
        "👇👇👇👇👇👇👇👇👇👇\n\n"
        "✨ **Aur agar aap aur videos dekhna chahte hain toh, yeh link join karein!** 🔥🔥\n\n"
        "👉 [https://t.me/imsha_rehman_allpartslink](https://t.me/imsha_rehman_allpartslink)\n\n"
        "👉 [https://t.me/imsha_rehman_allpartslink](https://t.me/imsha_rehman_allpartslink)\n\n"
        "👉 **Join karo aur maze le lo!** 😘"
    )
    await message.reply(text, reply_markup=create_keyboard())

@bot.on_message(filters.command("menu"))
async def menu(client, message):
    await message.reply("Menu:\n/start - Start the bot")

if __name__ == "__main__":
    bot.run()
