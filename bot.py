cat bot.py
import telebot                                  from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random                                   import os
import json
import yt_dlp
                                                TOKEN = "8975002390:AAEMcegism0UbYVNKwo82aCSNrj_CvNXf9M"
bot = telebot.TeleBot(TOKEN)                    
# 👑 آيدي المالك الأساسي
OWNER_ID = 1961113470
                                                ADMINS_FILE = "admins.json"
REPLIES_FILE = "replies.json"
SETTINGS_FILE = "settings.json"

# --- دوال حفظ واسترجاع البيانات ---
def load_data(file, default):
    if not os.path.exists(file):                        return default
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default                          
def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:        json.dump(data, f, ensure_ascii=False, indent=4)                                                                                        admins_list = load_data(ADMINS_FILE, [OWNER_ID])
custom_replies = load_data(REPLIES_FILE, {})
settings = load_data(SETTINGS_FILE, {"games_enabled": True})                                    
# حالة الخطوات (متابعة إدخال المالك بالخاص)
user_states = {}

# ==========================================
# 👑 لوحة التحكم الشفافة بالخاص (ستار)
# ==========================================
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda m: m.text and m.text.strip() == "ستار" and m.chat.type == "private")                                           def start_panel(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in admins_list:                                              bot.reply_to(message, "هذه اللوحة مخصصة لمالك وأدمنية البوت فقط! 🛑")
        return

    markup = InlineKeyboardMarkup(row_width=2)      markup.add(
        InlineKeyboardButton("🛡️ رفع أدمن بالآيدي", callback_data="add_admin_id"),
        InlineKeyboardButton("🗑️ تنزيل أدمن بالآيدي", callback_data="del_admin_id"),
        InlineKeyboardButton("➕ إضافة رد مخصص", callback_data="add_reply"),
        InlineKeyboardButton("📋 عرض/مسح الردود", callback_data="list_replies"),
        InlineKeyboardButton(f"🎮 التسلية: {'مفعلة ✅' if settings['games_enabled'] else 'معطلة ❌'}", callback_data="toggle_games"),
        InlineKeyboardButton("📊 إحصائيات البوت", callback_data="bot_stats")
    )
    bot.send_message(message.chat.id, "أهلاً بك في لوحة تحكم البوت الشاملة 🌟\nاختر من الأزرار أدناه للتحكم بالإعدادات:", reply_markup=markup)   
# معالجة ضغط الأزرار الشفافة                    @bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if user_id != OWNER_ID and user_id not in admins_list:
        bot.answer_callback_query(call.id, "غير مصرح لك!", show_alert=True)                             return
                                                    chat_id = call.message.chat.id
                                                    if call.data == "add_admin_id":
        user_states[user_id] = "waiting_for_admin_id"
        bot.send_message(chat_id, "أرسل الآن آيدي (ID) الشخص الذي تريد رفعه كأدمن في البوت:")           bot.answer_callback_query(call.id)
                                                    elif call.data == "del_admin_id":
        user_states[user_id] = "waiting_for_del_admin_id"
        bot.send_message(chat_id, "أرسل الآن آيدي (ID) الأدمن المراد تنزيله:")                          bot.answer_callback_query(call.id)
                                                    elif call.data == "add_reply":
        user_states[user_id] = "waiting_for_reply_trigger"
        bot.send_message(chat_id, "أرسل الكلمة أو العبارة التي تريد للبوت أن يستجيب لها:")              bot.answer_callback_query(call.id)
                                                    elif call.data == "list_replies":
        if not custom_replies:                              bot.send_message(chat_id, "لا توجد أي ردود مخصصة محفوظة حالياً.")
        else:
            text = "📋 **قائمة الردود المحفوظة:**\n\n"
            for trig in custom_replies.keys():
                text += f"• `{trig}`\n"
            bot.send_message(chat_id, text, parse_mode="Markdown")
        bot.answer_callback_query(call.id)

    elif call.data == "toggle_games":
        settings["games_enabled"] = not settings["games_enabled"]                                       save_data(SETTINGS_FILE, settings)
        bot.answer_callback_query(call.id, "تم تغيير حالة قسم التسلية!")                                start_panel(call.message)
                                                    elif call.data == "bot_stats":
        stats = f"📊 **إحصائيات البوت:**\n\n" \
                f"👤 عدد الأدمنية: {len(admins_list)}\n" \
                f"💬 عدد الردود المخصصة: {len(custom_replies)}\n" \
                f"🎮 قسم التسلية: {'مفعل' if settings['games_enabled'] else 'معطل'}"
        bot.send_message(chat_id, stats, parse_mode="Markdown")
        bot.answer_callback_query(call.id)
                                                
# ==========================================
# 📩 معالج الرسائل الخاصة (خطوات إدخال الإعدادات)
# ==========================================
@bot.message_handler(func=lambda m: m.chat.type == "private" and m.from_user.id in user_states) def handle_private_steps(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)            
    if state == "waiting_for_admin_id":                 if message.text and message.text.isdigit():
            new_admin = int(message.text)
            if new_admin not in admins_list:
                admins_list.append(new_admin)
                save_data(ADMINS_FILE, admins_list)                                                             bot.reply_to(message, f"تم رفع المستخدم `{new_admin}` كأدمن بنجاح! ✅", parse_mode="Markdown")
            else:                                               bot.reply_to(message, "هذا المستخدم أدمن بالفعل!")
            del user_states[user_id]
        else:                                               bot.reply_to(message, "الرجاء إرسال آيدي صحيح (أرقام فقط).")

    elif state == "waiting_for_del_admin_id":           if message.text and message.text.isdigit():
            target_admin = int(message.text)
            if target_admin == OWNER_ID:
                bot.reply_to(message, "لا يمكنك تنزيل المالك الأساسي! 😅")
            elif target_admin in admins_list:                   admins_list.remove(target_admin)
                save_data(ADMINS_FILE, admins_list)
                bot.reply_to(message, f"تم تنزيل الأدمن `{target_admin}` بنجاح! 📉", parse_mode="Markdown")                                                 else:
                bot.reply_to(message, "هذا الرقم ليس ضمن قائمة الأدمنية.")
            del user_states[user_id]
        else:
            bot.reply_to(message, "الرجاء إرسال آيدي صحيح.")
                                                    elif state == "waiting_for_reply_trigger":
        if message.text:
            trigger = message.text.strip()
            user_states[user_id] = {"state": "waiting_for_reply_content", "trigger": trigger}               bot.reply_to(message, f"ممتاز! الآن أرسل الرد للبوت عند كتابة `{trigger}`.", parse_mode="Markdown")
        else:                                               bot.reply_to(message, "يرجى إرسال الكلمة كنص.")
                                                    elif isinstance(state, dict) and state.get("state") == "waiting_for_reply_content":                 trigger = state["trigger"]
        if message.text:
            custom_replies[trigger] = {"type": "text", "content": message.text}                         elif message.photo:
            custom_replies[trigger] = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.caption}                               elif message.video:
            custom_replies[trigger] = {"type": "video", "file_id": message.video.file_id, "caption": message.caption}                                   elif message.voice:
            custom_replies[trigger] = {"type": "voice", "file_id": message.voice.file_id}
        elif message.sticker:
            custom_replies[trigger] = {"type": "sticker", "file_id": message.sticker.file_id}           elif message.document:
            custom_replies[trigger] = {"type": "document", "file_id": message.document.file_id, "caption": message.caption}
                                                        save_data(REPLIES_FILE, custom_replies)
        bot.reply_to(message, f"تم حفظ الرد للكلمة `{trigger}` بنجاح! 🎉", parse_mode="Markdown")
        del user_states[user_id]                
                                                # ==========================================
# 🛠️ معالج المجموعات (الحماية، البحث الموسيقي، والتسلية)
# ==========================================    @bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'voice', 'sticker', 'document'])
def group_handler(message):                         chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""                                         
    # --- 1. خيار البحث وتنزيل الأغاني والصوتيات (يوت) ---
    if text.startswith("يوت "):
        query = text[4:].strip()
        if not query:                                       bot.reply_to(message, "يرجى كتابة اسم الأغنية بعد كلمة يوت (مثال: يوت سلامات)")                 return

        msg = bot.reply_to(message, "🔎 جاري البحث والتنزيل من يوتيوب، انتظر لحظة...")

        try:                                                search_query = f"ytsearch1:{query}" 
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'song.%(ext)s',                      'postprocessors': [{                                'key': 'FFmpegExtractAudio',                    'preferredcodec': 'mp3',
                    'preferredquality': '192',                  }],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:                                                             info = ydl.extract_info(search_query, download=True)                                            if 'entries' in info:
                    video_title = info['entries'][0]['title']
                else:
                    video_title = info.get('title', 'مقطع صوتي')

            audio_file = "song.mp3"                         if os.path.exists(audio_file):
                with open(audio_file, 'rb') as audio:
                    bot.send_audio(chat_id, audio, caption=f"🎵 {video_title}", reply_to_message_id=message.message_id)                                         os.remove(audio_file)
                bot.delete_message(chat_id, msg.message_id)
            else:
                bot.edit_message_text("تعذر التحميل، تأكد من تثبيت مكتبة ffmpeg بشكل صحيح.", chat_id, msg.message_id)
        except Exception as e:                              bot.edit_message_text("حدث خطأ أثناء البحث أو التحميل 😅", chat_id, msg.message_id)
        return
                                                    # --- 2. الردود المخصصة ---
    if text in custom_replies:                          rep = custom_replies[text]
        rep_type = rep.get("type")                      if rep_type == "text":
            bot.reply_to(message, rep["content"])
        elif rep_type == "photo":
            bot.send_photo(chat_id, rep["file_id"], caption=rep.get("caption"), reply_to_message_id=message.message_id)
        elif rep_type == "video":
            bot.send_video(chat_id, rep["file_id"], caption=rep.get("caption"), reply_to_message_id=message.message_id)
        elif rep_type == "voice":
            bot.send_voice(chat_id, rep["file_id"], reply_to_message_id=message.message_id)
        elif rep_type == "sticker":                         bot.send_sticker(chat_id, rep["file_id"], reply_to_message_id=message.message_id)
        elif rep_type == "document":
            bot.send_document(chat_id, rep["file_id"], caption=rep.get("caption"), reply_to_message_id=message.message_id)
        return
                                                    # --- 3. أوامر الحماية والتقييد ---
    protection_commands = ["كتم", "تكلم", "فك الكتم", "حظر", "الغاء حظر", "فك الحظر", "طرد", "تقيد", "فك التقيد", "رفع مشرف", "تنزيل مشرف"]

    # معالجة رفع وتنزيل المشرف من الكروب مباشرة بالرد
    if text in ["رفع مشرف", "تنزيل مشرف"]:
        if user_id != OWNER_ID:
            bot.reply_to(message, "هذا الأمر مخصص لمالك البوت حصراً! 🛑")
            return
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
            if text == "رفع مشرف":
                if target_user not in admins_list:
                    admins_list.append(target_user)
                    save_data(ADMINS_FILE, admins_list)
                    bot.reply_to(message, "تم رفع العضو مشرفاً في البوت بنجاح 🛡️✨")
                else:
                    bot.reply_to(message, "هذا العضو مشرف بالفعل!")
            elif text == "تنزيل مشرف":
                if target_user == OWNER_ID:
                    bot.reply_to(message, "لا يمكنك تنزيل المالك الأساسي! 😅")
                elif target_user in admins_list:
                    admins_list.remove(target_user)                                                                 save_data(ADMINS_FILE, admins_list)
                    bot.reply_to(message, "تم تنزيل العضو من رتبة المشرف 🔽")                                   else:
                    bot.reply_to(message, "هذا العضو ليس ضمن قائمة المشرفين.")
        else:
            bot.reply_to(message, f"يرجى الرد على رسالة العضو واكتب ({text})")
        return

    # باقي أوامر الحماية                            if text in ["كتم", "تكلم", "فك الكتم", "حظر", "الغاء حظر", "فك الحظر", "طرد", "تقيد", "فك التقيد"]:                                                 if user_id not in admins_list and user_id != OWNER_ID:                                              bot.reply_to(message, "عذراً، هذه الأوامر للمشرفين والأدمنية فقط! 🚫")                           return
        if not message.reply_to_message:                    bot.reply_to(message, f"يرجى الرد على رسالة العضو واكتب ({text})")                              return

        target_user = message.reply_to_message.from_user.id                                     
        try:                                                if text == "كتم":
                bot.restrict_chat_member(chat_id, target_user, can_send_messages=False)                         bot.reply_to(message, "تم كتم العضو بنجاح 🔇")
            elif text in ["تكلم", "فك الكتم"]:                  bot.restrict_chat_member(chat_id, target_user, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
                bot.reply_to(message, "تم إلغاء كتم العضو 🔊")
            elif text == "حظر":
                bot.ban_chat_member(chat_id, target_user)
                bot.reply_to(message, "تم حظر العضو نهائياً 🚫")                                             elif text in ["الغاء حظر", "فك الحظر"]:                                                             bot.unban_chat_member(chat_id, target_user)                                                     bot.reply_to(message, "تم إلغاء الحظر عن العضو ✅")
            elif text == "طرد":                                 bot.ban_chat_member(chat_id, target_user, until_date=30)                                        bot.unban_chat_member(chat_id, target_user)
                bot.reply_to(message, "تم طرد العضو من المجموعة 👢")                                        elif text == "تقيد":
                bot.restrict_chat_member(chat_id, target_user, can_send_messages=True, can_send_media_messages=False, can_send_other_messages=False)                                                            bot.reply_to(message, "تم تقييد العضو من الوسائط والروابط ⚠️")
            elif text == "فك التقيد":
                bot.restrict_chat_member(chat_id, target_user, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
                bot.reply_to(message, "تم فك التقييد بنجاح ✅")
        except Exception:
            bot.reply_to(message, "خطأ: تأكد من صلاحيات البوت أو أن الشخص ليس مشرفاً.")                  return

    # --- 4. قسم التسلية والترفيه ---
    if settings.get("games_enabled", True):     
        if text in ["الألعاب", "اوامر التسلية", "التسلية"]:                                                 games_menu = (
                "🎮 **قائمة ألعاب البوت الشاملة والترفيه:**\n\n"
                "🎵 `يوت [اسم الأغنية]` ➔ للبحث وتنزيل ملف صوتي من يوتيوب 🎧\n"
                "1️⃣ `حظك` ➔ لتعرف حظك اليوم 🌟\n"
                "2️⃣ `نسبة الحب` ➔ (بالرد على شخص) لحساب نسبة الحب ❤️\n"                                           "3️⃣ `زواج` ➔ (بالرد على شخص) لتعرف نتيجة الزواج من الشخص 💍\n"
                "4️⃣ `صراحة` أو `انحراف` ➔ أسئلة صراحة وجريئة للوناسة ☕\n"                                       "5️⃣ `لو خيروك` ➔ خيارات صعبة وممتعة 🤔\n"
                "6️⃣ `نكتة` ➔ لتموت ضحك 😂\n"                     "7️⃣ `حكمة` ➔ حكمة اليوم 📜\n"
                "8️⃣ `مطور البوت` ➔ لمعرفة مطور البوت 👑"
            )
            bot.reply_to(message, games_menu)
            return

        elif text == "نسبة الحب":
            if message.reply_to_message:
                target_name = message.reply_to_message.from_user.first_name
                love_score = random.randint(15, 100)
                bot.reply_to(message, f"نسبة الحب بينك وبين {target_name} هي: {love_score}% ❤️🔥")
            else:
                bot.reply_to(message, "سوي رد على رسالة الشخص واكتب (نسبة الحب)!")
            return

        elif text == "زواج":
            if message.reply_to_message:                        target_name = message.reply_to_message.from_user.first_name
                status_list = [
                    f"مبروك! تزوجت انت و {target_name} وصار عدكم 4 جهال 👶💍",
                    f"للأسف الطلب مرفوض، {target_name} انطاك حظر وراحت عليك 💔😂",
                    f"عقد قران مبارك! راح تروحون بشهر عسل لماليزيا ✈️🌴",
                    f"صار خطوبة بس العروس هربت بيوم العرس! 🏃‍♀️💨"                                               ]
                bot.reply_to(message, random.choice(status_list))
            else:
                bot.reply_to(message, "رد على رسالة الشخص واكتب (زواج) حتى تتم مراسم العقد! 💍")            return
                                                        elif text == "حظك":
            luck_list = [
                "حظك اليوم ممتاز جداً وتحس بفرصة ذهبية! 🌟",
                "حظك متوسط، تجنب المشاكل اليوم وابقى هادئاً ☕",
                "اليوم حظك سيء، لا تتخذ أي قرار مهم 😅",                                                        "أنت محظوظ اليوم، اضحك واستانس! 🎉",
                "الأمور تبدو مذهلة ومشرقة بالنسبة لك اليوم! ✨"
            ]                                               bot.reply_to(message, random.choice(luck_list))                                                 return
                                                        elif text in ["صراحة", "انحراف"]:
            questions = [                                       "شنو أكثر موقف محرج صار بحياتك؟ 😳",                                                            "لو انطوك مليون دولار بس تترك الموبايل شهر، توافق؟ 📱",                                         "منو أكثر شخص تكرهه بالكروب؟ (بدون فضح) 😂",                                                    "شنو أكتر أكلة تموت عليها؟ 🍕",
                "لو خيروك تعيش بلا نت أو بلا أصدقاء شتختار؟ 🤔"
            ]                                               bot.reply_to(message, f"🎯 **سؤال صراحة لك:**\n\n{random.choice(questions)}")                   return
                                                        elif text == "لو خيروك":
            choices = [                                         "لو خيروك: تاكل أكل حار كلش يكتلك بالعصارة لو تشرب مي بحر؟ 🌶️🌊",                                "لو خيروك: تختفي يوم كامل لو تقرأ أفكار الناس؟ 👻🧠",                                           "لو خيروك: تنام بالشارع لو تلبس ملابس صيفية بالشتاء؟ 🧥❄️"                                   ]
            bot.reply_to(message, f"🤔 **لو خيروك:**\n\n{random.choice(choices)}")
            return                              
        elif text == "نكتة":                                jokes = [
                "واحد غبي كالوا له انطيني بيت بحرف الـ ح، كال: حوش واسع! 😂",
                "مرة واحد دخل صيدلية كال عندك علاج للنسيان؟ الصيدلي كال إي، الغبي كال زين شسمه؟ 😭",                                                            "واحد يكول لزوجته: تدرين إني تزوجتك علمود جمالك لو عقلج؟ كتله: لا، علمود عيوني الحلوات! 🏃‍♂️"
            ]                                               bot.reply_to(message, random.choice(jokes))                                                     return
                                                        elif text == "حكمة":
            wisdoms = [                                         "من تسرّع في الجواب، أخطأ في الصواب 📜",                                                         "الصمت زينة والجهل ميناء السلامة 🧠",                                                           "إذا كان الكلام من فضة فالسكوت من ذهب ✨"                                                   ]
            bot.reply_to(message, f"📜 **حكمة اليوم:**\n\n{random.choice(wisdoms)}")
            return                              
        elif text in ["مطور البوت", "المطور"]:              bot.reply_to(message, "👑 مطور هذا البوت ومالكه هو تاج الراس **سِجّيَلَ** 😎✨")                    return
                                                print("البوت يعمل بكامل طاقته وجهوزيته...")
bot.infinity_polling()
