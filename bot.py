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
bot = Client("premium_x_hub_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["premium_x_hub"]
users_collection = db["users"]

def add_user(user_id, referred_by=None):
    if not users_collection.find_one({"user_id": user_id}):
        user_data = {
            "user_id": user_id,
            "points": 0,
            "referred_by": referred_by,
        }
        users_collection.insert_one(user_data)
        if referred_by:
            users_collection.update_one(
                {"user_id": referred_by},
                {"$inc": {"points": 2}}  # Referral reward updated to 2 points
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

    if len(message.text.split()) > 1:
        try:
            referred_by = int(message.text.split()[1])
        except ValueError:
            pass

    add_user(user_id, referred_by)

    text = (
        f"🌟 **Welcome to Premium X Hub, {message.from_user.first_name}!** 🌟\n\n"
        "🎉 **Get ready to explore premium content** from top platforms like:\n"
        "- **OnlyFans Premium**\n"
        "- **Pornhub Premium**\n"
        "- **TikTok Videos**\n"
        "- **Exclusive VIP Content**\n"
        "- **And much more!** 🔥\n\n"
        "✨ **What’s Inside?**\n"
        "- A wide range of exciting, high-quality videos and content waiting for you.\n"
        "- **No subscriptions required**, just instant access to everything!\n\n"
        "🎁 **Your Options:**\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 Browse Content Categories", callback_data="browse_categories")],
        [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
    ])

    await message.reply(text, reply_markup=keyboard)

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    bot_username = (await bot.get_me()).username

    if callback_query.data == "browse_categories":
        text = (
            "📂 **Choose a category to explore:**\n\n"
            "1️⃣ **OnlyFans Premium**\n"
            "2️⃣ **Pornhub Premium**\n"
            "3️⃣ **TikTok Videos**\n"
            "4️⃣ **Exclusive Content**\n"
            "5️⃣ **VIP Content Access**\n\n"
            "🎁 **Your Options:**\n"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("1️⃣ OnlyFans Premium", callback_data="onlyfans")],
            [InlineKeyboardButton("2️⃣ Pornhub Premium", callback_data="pornhub")],
            [InlineKeyboardButton("3️⃣ TikTok Videos", callback_data="tiktok")],
            [InlineKeyboardButton("4️⃣ Exclusive Content", callback_data="exclusive")],
            [InlineKeyboardButton("5️⃣ VIP Content Access", callback_data="vip")],
            [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
        ])
        await callback_query.message.edit(text, reply_markup=keyboard)

    elif callback_query.data in ["onlyfans", "pornhub", "tiktok", "exclusive", "vip"]:
        points = get_user_points(user_id)

        if points >= 5:  # Points requirement updated to 5
            # Unlock content
            text = f"🎉 **You've unlocked {callback_query.data.capitalize()} Content!**\n\n" \
                   "Enjoy premium content:\n" \
                   "- 🔥 [Link 1](https://example.com/1)\n" \
                   "- 🔥 [Link 2](https://example.com/2)\n" \
                   "- 🔥 [Link 3](https://example.com/3)\n\n" \
                   "🎁 **Your Options:**"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📂 Browse Content Categories", callback_data="browse_categories")],
                [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
            ])
        else:
            text = (
                "❌ **You don't have enough points to unlock this content.**\n\n"
                "📢 **To unlock this content, you need 5 points.**\n\n"
                "🎁 **How to earn points?**\n"
                "Invite your friends to join this bot using your referral link. For every friend who joins, you'll earn **2 points**!\n\n"
                "🎁 **Your Options:**"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Get Your Referral Link", callback_data="referral_link")],
                [InlineKeyboardButton("🎯 Check Your Points", callback_data="check_points")],
                [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
            ])

        await callback_query.message.edit(text, reply_markup=keyboard)

    elif callback_query.data == "referral_link":
        referral_link = get_referral_link(bot_username, user_id)
        await bot.send_message(
            callback_query.from_user.id,
            f"🔗 **Your Referral Link:**\n{referral_link}\n\n"
            "🎁 **Your Options:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Check Your Points", callback_data="check_points")],
                [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
            ])
        )

    elif callback_query.data == "check_points":
        points = get_user_points(user_id)
        await bot.send_message(
            callback_query.from_user.id,
            f"🎁 **Your Current Points:** {points}\n\n"
            "📢 **You need 5 points to unlock premium content.** Keep inviting your friends to earn more points.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Get Your Referral Link", callback_data="referral_link")],
                [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
            ])
        )

    elif callback_query.data == "help":
        await bot.send_message(
            callback_query.from_user.id,
            "**Here's how to use Premium X Hub Bot:**\n\n"
            "1. **Browse Categories**: Explore premium content in different categories.\n"
            "2. **Earn Points**: Share your referral link and earn 2 points for each friend who joins.\n"
            "3. **Unlock Content**: Use 5 points to unlock premium content in various categories.\n\n"
            "**Commands:**\n"
            "/start - Start the bot\n"
            "/help - Get help",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 Need Help?", callback_data="help")]
            ])
        )

    await callback_query.answer()

if __name__ == "__main__":
    bot.run()
