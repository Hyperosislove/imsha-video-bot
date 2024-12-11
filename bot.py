import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
MONGO_URI = os.getenv("MONGO_URI")

# Initialize bot client
bot = Client("referral_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["referral_bot"]
users_collection = db["users"]

def add_user(user_id, referred_by=None):
    # Add user if not already exists
    if not users_collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "points": 0,
            "referred_by": referred_by,
        }
        users_collection.insert_one(user_data)
        # Increment points for the referrer
        if referred_by:
            users_collection.update_one(
                {"user_id": referred_by},
                {"$inc": {"points": 1}}
            )

def get_user_points(user_id):
    user = users_collection.find_one({"user_id": user_id})
    return user["points"] if user else 0

def get_referral_link(bot_username, user_id):
    return f"https://t.me/{bot_username}?start={user_id}"

@bot.on_message(filters.command(["start", "help"]))
async def start(client, message):
    bot_username = (await bot.get_me()).username
    user_id = message.from_user.id
    referred_by = None

    # If the user starts with a referral link
    if len(message.text.split()) > 1:
        try:
            referred_by = int(message.text.split()[1])
        except ValueError:
            pass

    # Add user to the database
    add_user(user_id, referred_by)

    # Fetch user's points
    points = get_user_points(user_id)

    # Generate referral link
    referral_link = get_referral_link(bot_username, user_id)

    # Image URL
    image_url = "https://i.imgur.com/0KLPahJ.jpg"  # Use the new image URL

    # Message to user
    text = (
        f"🌟 **Welcome, {message.from_user.first_name}!** 🌟\n\n"
        "**How to Unlock All Content?**\n"
        "Explore premium content after earning points! Simply engage with the bot and enjoy exclusive offers.\n\n"
        f"🎁 **Your Current Points:** {points}\n\n"
        "Unlock exclusive content by earning points.\n"
    )

    # Send the welcome message with the image
    await bot.send_photo(message.chat.id, image_url, caption=text)

    # Add a keyboard markup with all options visible
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Check Points", callback_data="check_points")],
        [InlineKeyboardButton("🔗 Referral Link", callback_data="referral_link")], 
        [InlineKeyboardButton("🔓 Unlock Content", callback_data="unlock_content")],
        [InlineKeyboardButton("❓ Help", callback_data="help")] 
    ])
    
    # Send the buttons as a reply to the user
    await message.reply(text, reply_markup=keyboard)

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id 
    if callback_query.data == "check_points":
        points = get_user_points(user_id)
        await bot.send_message(
            callback_query.from_user.id,
            f"🎁 **Your Current Points:** {points}\n\n"
            "📢 **Invite more friends to earn points.** Use your referral link to unlock content!"
        )
    elif callback_query.data == "referral_link":
        bot_username = (await bot.get_me()).username
        referral_link = get_referral_link(bot_username, user_id)
        await bot.send_message(
            callback_query.from_user.id,
            f"🔗 **Your Referral Link:** \n{referral_link}"
        )
    elif callback_query.data == "unlock_content":
        points = get_user_points(user_id)

        if points >= 10:
            await bot.send_message(
                callback_query.from_user.id,
                "🎉 **Congratulations! You have unlocked exclusive content.**\n\n"
                "**Access Links:**\n"
                "- OnlyFans Premium: [Link](https://example.com/1)\n"
                "- Pornhub Premium: [Link](https://example.com/2)\n"
                "- TikTok Videos: [Link](https://example.com/3)\n"
                "\nKeep inviting friends to enjoy more rewards!"
            )
        else:
            await bot.send_message(
                callback_query.from_user.id,
                "❌ **You don't have enough points to unlock content.**\n\n"
                "📢 **Earn 10 points by inviting your friends using your referral link.**"
            )
    elif callback_query.data == "help":
        await bot.send_message(
            callback_query.from_user.id,
            "**Here's how to use this bot:**\n\n"
            "1. **Invite friends:** Share your referral link with friends.\n"
            "2. **Earn points:** Get 1 point for each friend who joins.\n"
            "3. **Unlock content:** Use 10 points to unlock exclusive content.\n\n"
            "**Commands:**\n"
            "/start - Start the bot\n"
            "/points - Check your points\n"
            "/unlock - Unlock content\n"
            "/help - Get help"
        )

    await callback_query.answer() # Acknowledge the callback query

if __name__ == "__main__":
    bot.run()
