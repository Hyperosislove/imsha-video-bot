import os
from pyrogram import Client, filters
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

@bot.on_message(filters.command("start"))
async def start(client, message):
    bot_username = (await bot.get_me()).username
    user_id = message.from_user.id
    referred_by = None

    # If the user starts with a referral link
    if len(message.command) > 1:
        try:
            referred_by = int(message.command[1])
        except ValueError:
            pass

    # Add user to the database
    add_user(user_id, referred_by)

    # Fetch user's points
    points = get_user_points(user_id)

    # Generate referral link
    referral_link = get_referral_link(bot_username, user_id)

    # Message to user
    text = (
        f"🌟 **Welcome, {message.from_user.first_name}!** 🌟\n\n"
        "**How to Unlock All Content?**\n"
        "Invite your friends to use this bot. For every friend who joins using your referral link, you'll earn **1 point**.\n\n"
        "📌 **Referral Link:**\n{referral_link}\n\n"
        f"🎁 **Your Current Points:** {points}\n\n"
        "🔓 **Unlock Content:** Earn 1 point to unlock all content!"
    )
    await message.reply(text)

@bot.on_message(filters.command("points"))
async def check_points(client, message):
    user_id = message.from_user.id
    points = get_user_points(user_id)
    await message.reply(
        f"🎁 **Your Current Points:** {points}\n\n"
        "📢 **Invite more friends to earn points.** Use your referral link to unlock content!"
    )

@bot.on_message(filters.command("unlock"))
async def unlock_content(client, message):
    user_id = message.from_user.id
    points = get_user_points(user_id)

    if points >= 1:
        await message.reply(
            "🎉 **Congratulations! You have unlocked all content.**\n\n"
            "**Access Links:**\n"
            "- Content 1: [Link](https://example.com/1)\n"
            "- Content 2: [Link](https://example.com/2)\n"
            "- Content 3: [Link](https://example.com/3)\n"
            "\nKeep inviting friends to enjoy more rewards!"
        )
    else:
        await message.reply(
            "❌ **You don't have enough points to unlock content.**\n\n"
            "📢 **Earn 1 point by inviting your friends using your referral link.**"
        )

if __name__ == "__main__":
    bot.run()
