import telebot
from telebot import types
import time

# আপনার তথ্য
API_TOKEN = '8546448640:AAE3ct_O6fTUjx4s1YVkTvmoiy3AElHURro'
ADMIN_ID = 6220609091 
# লিঙ্ক দুটি এখানে বসান
MONETAG_LINK = "https://otieu.com/4/10255176"
ADSTERRA_LINK = "https://www.effectivegatecpm.com/fny4t1sx?key=16a57612cfdc074e5a6e2c5d5c0c93fd"

# আপনার চ্যানেলের ইউজারনেম
CHANNELS = ["@business612", "@adsnetwork01"] 

bot = telebot.TeleBot(API_TOKEN)
users = {} 

def is_subscribed(chat_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, chat_id).status
            if status == 'left':
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    if uid not in users:
        users[uid] = {'bal': 0, 'ref': 0, 'last_bonus': 0}
        referrer = message.text.split()
        if len(referrer) > 1 and int(referrer[1]) != uid:
            ref_id = int(referrer[1])
            if ref_id in users:
                users[ref_id]['bal'] += 2
                users[ref_id]['ref'] += 1
                bot.send_message(ref_id, "🔔 কেউ আপনার লিঙ্কে জয়েন করেছে! আপনি ২ টাকা পেয়েছেন।")

    if is_subscribed(uid):
        show_main_menu(uid)
    else:
        show_force_join(uid)

def show_force_join(uid):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📢 চ্যানেল ১", url=f"https://t.me/{CHANNELS[0][1:]}")
    btn2 = types.InlineKeyboardButton("📢 চ্যানেল ২", url=f"https://t.me/{CHANNELS[1][1:]}")
    btn_check = types.InlineKeyboardButton("✅ জয়েন করেছি (Check)", callback_data="check_join")
    markup.add(btn1, btn2)
    markup.add(btn_check)
    bot.send_message(uid, "❌ আপনি আমাদের চ্যানেলে জয়েন করেননি!\n\nবটটি ব্যবহার করতে নিচের দুটি চ্যানেলে জয়েন করে 'Check' বাটনে ক্লিক করুন।", reply_markup=markup)

def show_main_menu(uid):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("💰 কাজ করুন", "🎁 ডেইলি বোনাস", "👤 প্রোফাইল", "👫 রেফার", "💸 উইথড্র")
    bot.send_message(uid, "স্বাগতম! এখন আপনি কাজ শুরু করতে পারেন।", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    uid = m.chat.id
    if uid not in users: return
    if not is_subscribed(uid):
        show_force_join(uid)
        return

    if m.text == "💰 কাজ করুন":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_monetag = types.InlineKeyboardButton("🔥 কাজ ১ (Monetag)", url=MONETAG_LINK)
        btn_adsterra = types.InlineKeyboardButton("⚡ কাজ ২ (Adsterra)", url=ADSTERRA_LINK)
        claim_btn = types.InlineKeyboardButton("✅ রিওয়ার্ড নিন (Claim)", callback_data="claim")
        markup.add(btn_monetag, btn_adsterra, claim_btn)
        bot.send_message(uid, "নিচের যেকোনো একটি লিঙ্কে ক্লিক করে অ্যাড দেখুন, তারপর রিওয়ার্ড নিন।", reply_markup=markup)

    elif m.text == "🎁 ডেইলি বোনাস":
        now = time.time()
        if now - users[uid]['last_bonus'] > 86400:
            users[uid]['bal'] += 1
            users[uid]['last_bonus'] = now
            bot.send_message(uid, "অভিনন্দন! আপনি ১ টাকা ডেইলি বোনাস পেয়েছেন।")
        else:
            bot.send_message(uid, "আপনি আজ বোনাস নিয়েছেন। আগামীকাল আবার আসুন।")

    elif m.text == "👤 প্রোফাইল":
        msg = f"🆔 আইডি: {uid}\n💰 ব্যালেন্স: {users[uid]['bal']} টাকা\n👫 মোট রেফার: {users[uid]['ref']}"
        bot.send_message(uid, msg)

    elif m.text == "👫 রেফার":
        ref_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        bot.send_message(uid, f"আপনার রেফার লিঙ্ক:\n{ref_link}\n\nপ্রতি রেফারে পাবেন ২ টাকা।")

    elif m.text == "💸 উইথড্র":
        if users[uid]['bal'] >= 50:
            bot.send_message(uid, "আপনার বিকাশ নম্বর দিন। এডমিন চেক করে পেমেন্ট করবে।")
        else:
            bot.send_message(uid, "উইথড্রর জন্য কমপক্ষে ৫০ টাকা লাগবে।")

@bot.callback_query_handler(func=lambda call: True)
def callback_all(call):
    uid = call.message.chat.id
    if call.data == "check_join":
        if is_subscribed(uid):
            bot.delete_message(uid, call.message.message_id)
            show_main_menu(uid)
        else:
            bot.answer_callback_query(call.id, "⚠️ আপনি এখনও সব চ্যানেলে জয়েন করেননি!", show_alert=True)
    elif call.data == "claim":
        users[uid]['bal'] += 0.5
        bot.answer_callback_query(call.id, "০.৫ টাকা যোগ হয়েছে!")
        bot.edit_message_text("কাজ সম্পন্ন! আবার কাজ করতে বাটনে চাপ দিন।", uid, call.message.message_id)

bot.polling()
