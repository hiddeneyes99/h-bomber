"""
============================================
ADMIN PANEL MODULE - COMPLETE
============================================
Telegram Bot Admin Panel with all management features

Features:
- Number Protection Management
- User Ban/Unban System
- User Allow/Disallow Access Control
- Credit Management System
- Redeem Code Generation
- Broadcasting System
- User List Management

Author: Your Name
Date: 2024
"""

from functools import wraps
from telebot import types
import time
import datetime


# ===============================================
# ADMIN KEYBOARDS
# ===============================================

def admin_kb():
    """
    Creates the main admin panel keyboard with all management options
    
    Returns:
        ReplyKeyboardMarkup: Admin panel keyboard
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("➕ Protect Number"), types.KeyboardButton("➖ Unprotect Number"))
    kb.add(types.KeyboardButton("🚷 Ban User"), types.KeyboardButton("🚳 Unban User"))
    kb.add(types.KeyboardButton("➕ Allow User"), types.KeyboardButton("➖ Disallow User"))
    kb.add(types.KeyboardButton("📜 Protected List"), types.KeyboardButton("📵 Banned List"))
    kb.add(types.KeyboardButton("🔒 Allowed List"), types.KeyboardButton("👥 Users"))
    kb.add(types.KeyboardButton("➕ Give Credit"), types.KeyboardButton("🔁 Gen Redeem Code"))
    kb.add(types.KeyboardButton("📜 Redeem Codes"), types.KeyboardButton("📊 Credits"))
    kb.add(types.KeyboardButton("📣 Broadcast"), types.KeyboardButton("⬅️ Back"))
    return kb


# ===============================================
# ADMIN DECORATOR
# ===============================================

def require_owner(func):
    """
    Decorator to restrict access to owner only
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with owner check
    """
    @wraps(func)
    def wrapper(m, *args, **kwargs):
        if m.from_user.id != OWNER_ID:
            return bot.send_message(m.chat.id, "🚫 You are not authorized to use this command.")
        return func(m, *args, **kwargs)
    return wrapper


# ===============================================
# ADMIN COMMAND HANDLERS
# ===============================================

def register_admin_handlers(bot_instance, owner_id, user_state_dict, main_menu_func, 
                           get_protected_list_func, get_banned_list_func, 
                           get_allowed_list_func, get_all_users_func,
                           normalize_mobile_func, is_protected_func, 
                           protect_number_func, unprotect_number_func,
                           ban_user_db_func, unban_user_db_func,
                           allow_user_func, disallow_user_func,
                           get_user_credits_func, set_user_credits_func,
                           gen_redeem_code_func, cur_db, conn_db):
    """
    Register all admin handlers to the bot
    
    Args:
        bot_instance: Telebot instance
        owner_id: Owner's Telegram ID
        user_state_dict: Dictionary to track user states
        main_menu_func: Function to generate main menu
        ... (other required functions)
    """
    global bot, OWNER_ID, USER_STATE, main_menu
    global get_protected_list, get_banned_list, get_allowed_list, get_all_users
    global normalize_mobile, is_protected, protect_number, unprotect_number
    global ban_user_db, unban_user_db, allow_user, disallow_user
    global get_user_credits, set_user_credits, gen_redeem_code
    global cur, conn
    
    bot = bot_instance
    OWNER_ID = owner_id
    USER_STATE = user_state_dict
    main_menu = main_menu_func
    get_protected_list = get_protected_list_func
    get_banned_list = get_banned_list_func
    get_allowed_list = get_allowed_list_func
    get_all_users = get_all_users_func
    normalize_mobile = normalize_mobile_func
    is_protected = is_protected_func
    protect_number = protect_number_func
    unprotect_number = unprotect_number_func
    ban_user_db = ban_user_db_func
    unban_user_db = unban_user_db_func
    allow_user = allow_user_func
    disallow_user = disallow_user_func
    get_user_credits = get_user_credits_func
    set_user_credits = set_user_credits_func
    gen_redeem_code = gen_redeem_code_func
    cur = cur_db
    conn = conn_db
    
    # Register handlers
    _register_handlers()


def _register_handlers():
    """Internal function to register all handlers"""
    
    @bot.message_handler(commands=["admin"])
    def cmd_admin(m):
        """Open admin panel via /admin command"""
        if m.from_user.id != OWNER_ID:
            return bot.send_message(m.chat.id, "🚫 Not authorized.")
        bot.send_message(m.chat.id, "👑 Admin Panel:", reply_markup=admin_kb())

    @bot.message_handler(func=lambda m: m.text == "🛠 Admin Panel")
    @require_owner
    def admin_panel_button(m):
        """Open admin panel via keyboard button"""
        bot.send_message(m.chat.id, "👑 Admin Panel:", reply_markup=admin_kb())

    # ===============================================
    # PROTECT/UNPROTECT NUMBER HANDLERS
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "➕ Protect Number")
    @require_owner
    def protect_prompt(m):
        """Prompt to protect a number"""
        USER_STATE[m.from_user.id] = "protect"
        bot.send_message(m.chat.id, "📲 Send number to protect (10 digits):")

    @bot.message_handler(func=lambda m: m.text == "➖ Unprotect Number")
    @require_owner
    def unprotect_prompt(m):
        """Prompt to unprotect a number"""
        USER_STATE[m.from_user.id] = "unprotect"
        bot.send_message(m.chat.id, "📲 Send number to unprotect (10 digits):")

    @bot.message_handler(func=lambda m: m.text == "📜 Protected List")
    @require_owner
    def show_protected(m):
        """Show list of all protected numbers"""
        try:
            data = get_protected_list()
            if not data:
                bot.send_message(m.chat.id, "📜 No protected numbers.")
            else:
                lines = [f"🔒 {row[0]} — by {row[1]} at {row[2]}" for row in data[:100]]
                msg = "🔒 Protected Numbers:\n\n" + "\n".join(lines)
                if len(data) > 100:
                    msg += f"\n\n... and {len(data) - 100} more numbers"
                bot.send_message(m.chat.id, msg)
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ Error: {str(e)}")

    # ===============================================
    # BAN/UNBAN USER HANDLERS
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "🚷 Ban User")
    @require_owner
    def ban_prompt(m):
        """Prompt to ban a user"""
        USER_STATE[m.from_user.id] = "ban"
        bot.send_message(m.chat.id, "🛑 Send Telegram user ID to ban (digits only):")

    @bot.message_handler(func=lambda m: m.text == "🚳 Unban User")
    @require_owner
    def unban_prompt(m):
        """Prompt to unban a user"""
        USER_STATE[m.from_user.id] = "unban"
        bot.send_message(m.chat.id, "✅ Send Telegram user ID to unban (digits only):")

    @bot.message_handler(func=lambda m: m.text == "📵 Banned List")
    @require_owner
    def show_banned(m):
        """Show list of all banned users"""
        try:
            data = get_banned_list()
            if not data:
                bot.send_message(m.chat.id, "📵 No banned users.")
            else:
                lines = [f"🚫 {row[0]} — by {row[1]} at {row[2]}" for row in data[:100]]
                msg = "🚫 Banned Users:\n\n" + "\n".join(lines)
                if len(data) > 100:
                    msg += f"\n\n... and {len(data) - 100} more users"
                bot.send_message(m.chat.id, msg)
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ Error: {str(e)}")

    # ===============================================
    # ALLOW/DISALLOW USER HANDLERS
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "➕ Allow User")
    @require_owner
    def allow_prompt(m):
        """Prompt to allow a user"""
        USER_STATE[m.from_user.id] = "allow"
        bot.send_message(m.chat.id, "➕ Send Telegram user ID to allow (digits only):")

    @bot.message_handler(func=lambda m: m.text == "➖ Disallow User")
    @require_owner
    def disallow_prompt(m):
        """Prompt to disallow a user"""
        USER_STATE[m.from_user.id] = "disallow"
        bot.send_message(m.chat.id, "➖ Send Telegram user ID to disallow (digits only):")

    @bot.message_handler(func=lambda m: m.text == "🔒 Allowed List")
    @require_owner
    def show_allowed(m):
        """Show list of all allowed users"""
        try:
            rows = get_allowed_list()
            if not rows:
                bot.send_message(m.chat.id, "🔒 No allowed users.")
            else:
                lines = [f"✅ {row[0]} — by {row[1]} at {row[2]}" for row in rows[:100]]
                msg = "🔒 Allowed Users:\n\n" + "\n".join(lines)
                if len(rows) > 100:
                    msg += f"\n\n... and {len(rows) - 100} more users"
                bot.send_message(m.chat.id, msg)
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ Error: {str(e)}")

    # ===============================================
    # USERS LIST HANDLER
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "👥 Users")
    @require_owner
    def show_users(m):
        """Show list of all bot users"""
        try:
            rows = get_all_users()
            if not rows:
                bot.send_message(m.chat.id, "👥 No users yet.")
            else:
                lines = []
                for r in rows[:100]:
                    username = f"@{r[1]}" if r[1] else "No username"
                    first_name = r[2] or ""
                    last_name = r[3] or ""
                    full_name = f"{first_name} {last_name}".strip()
                    lines.append(f"🆔 {r[0]} — {username} — {full_name}")
                
                msg = "👥 Known Users:\n\n" + "\n".join(lines)
                if len(rows) > 100:
                    msg += f"\n\n... and {len(rows) - 100} more users"
                bot.send_message(m.chat.id, msg)
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ Error: {str(e)}")

    # ===============================================
    # CREDIT MANAGEMENT HANDLERS
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "➕ Give Credit")
    @require_owner
    def give_credit_prompt(m):
        """Prompt to give credits to a user"""
        USER_STATE[m.from_user.id] = "give_credit"
        bot.send_message(m.chat.id, 
                         "➕ Give Credits\n\n"
                         "Format: <user_id> <amount> <days>\n"
                         "Example: 7729163608 5 30\n\n"
                         "• days=0 means credits never expire\n"
                         "• days>0 means credits expire after that many days")

    @bot.message_handler(func=lambda m: m.text == "📊 Credits")
    @require_owner
    def credits_prompt(m):
        """Prompt to check user credits"""
        USER_STATE[m.from_user.id] = "show_credits"
        bot.send_message(m.chat.id, 
                         "📊 Check Credits\n\n"
                         "• Send user ID to check specific user\n"
                         "• Send 'ALL' to list all users with credits")

    # ===============================================
    # REDEEM CODE HANDLERS
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "🔁 Gen Redeem Code")
    @require_owner
    def gen_redeem_prompt(m):
        """Prompt to generate redeem code"""
        USER_STATE[m.from_user.id] = "gen_redeem"
        bot.send_message(m.chat.id, 
                         "🔁 Generate Redeem Code\n\n"
                         "Format: <amount> <days>\n"
                         "Example: 3 7\n\n"
                         "This creates a code that gives:\n"
                         "• 3 credits\n"
                         "• Valid for 7 days\n"
                         "• days=0 means never expire")

    @bot.message_handler(func=lambda m: m.text == "📜 Redeem Codes")
    @require_owner
    def list_redeem_codes(m):
        """Show list of all redeem codes"""
        try:
            cur.execute("SELECT code, amount, days, created_by, created_at, used_by FROM redeem_codes ORDER BY created_at DESC")
            rows = cur.fetchall()
            
            if not rows:
                return bot.send_message(m.chat.id, "📜 No redeem codes found.")
            
            lines = ["🔁 Redeem Codes:\n"]
            for r in rows[:50]:
                code, amount, days, created_by, created_at, used_by = r
                status = "✅ Used" if used_by else "⏳ Unused"
                expire_info = f"{days} days" if days > 0 else "Never"
                lines.append(
                    f"\n📋 Code: {code}\n"
                    f"💰 Amount: {amount} credits\n"
                    f"⏱ Valid: {expire_info}\n"
                    f"👤 Created by: {created_by}\n"
                    f"📅 Created: {created_at}\n"
                    f"Status: {status}"
                )
            
            msg = "\n".join(lines)
            if len(rows) > 50:
                msg += f"\n\n... and {len(rows) - 50} more codes"
            
            bot.send_message(m.chat.id, msg)
        except Exception as e:
            bot.send_message(m.chat.id, f"❌ Error: {str(e)}")

    # ===============================================
    # BROADCAST HANDLER
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "📣 Broadcast")
    @require_owner
    def broadcast_prompt(m):
        """Prompt to broadcast message"""
        USER_STATE[m.from_user.id] = "broadcast"
        bot.send_message(m.chat.id, 
                         "📣 Broadcast Message\n\n"
                         "Send the message you want to broadcast to all users.\n"
                         "⚠️ This will send to ALL known users!")

    # ===============================================
    # BACK BUTTON HANDLER
    # ===============================================

    @bot.message_handler(func=lambda m: m.text == "⬅️ Back")
    @require_owner
    def back_to_main(m):
        """Return to main menu"""
        USER_STATE.pop(m.from_user.id, None)
        bot.send_message(m.chat.id, "↩️ Returning to main menu...", 
                         reply_markup=main_menu(is_owner=True))


# ===============================================
# ADMIN STATE PROCESSOR
# ===============================================

def process_admin_states(m, uid, txt):
    """
    Process admin panel state inputs
    Call this from your main text_handler
    
    Args:
        m: Message object
        uid: User ID
        txt: Message text
        
    Returns:
        bool: True if state was processed, False otherwise
    """
    state = USER_STATE.get(uid)
    
    if not state:
        return False
    
    # ===============================================
    # PROTECT NUMBER STATE
    # ===============================================
    if state == "protect":
        USER_STATE.pop(uid, None)
        num = normalize_mobile(txt)
        if not num:
            bot.send_message(uid, "❌ Invalid number format. Must be 10 digits.")
            return True
        if is_protected(num):
            bot.send_message(uid, f"⚠️ {num} is already protected.")
            return True
        protect_number(num, uid)
        bot.send_message(uid, f"✅ Protected: {num}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # UNPROTECT NUMBER STATE
    # ===============================================
    elif state == "unprotect":
        USER_STATE.pop(uid, None)
        num = normalize_mobile(txt)
        if not num:
            bot.send_message(uid, "❌ Invalid number format. Must be 10 digits.")
            return True
        if not is_protected(num):
            bot.send_message(uid, f"⚠️ {num} is not protected.")
            return True
        unprotect_number(num)
        bot.send_message(uid, f"✅ Unprotected: {num}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # BAN USER STATE
    # ===============================================
    elif state == "ban":
        USER_STATE.pop(uid, None)
        if not txt.isdigit():
            bot.send_message(uid, "❌ Invalid user ID. Must be digits only.")
            return True
        target = int(txt)
        if target == OWNER_ID:
            bot.send_message(uid, "⚠️ Cannot ban the owner!")
            return True
        ban_user_db(target, uid)
        bot.send_message(uid, f"🚫 Banned user: {target}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # UNBAN USER STATE
    # ===============================================
    elif state == "unban":
        USER_STATE.pop(uid, None)
        if not txt.isdigit():
            bot.send_message(uid, "❌ Invalid user ID. Must be digits only.")
            return True
        target = int(txt)
        unban_user_db(target)
        bot.send_message(uid, f"✅ Unbanned user: {target}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # ALLOW USER STATE
    # ===============================================
    elif state == "allow":
        USER_STATE.pop(uid, None)
        if not txt.isdigit():
            bot.send_message(uid, "❌ Invalid user ID. Must be digits only.")
            return True
        target = int(txt)
        if allow_user(target, uid):
            bot.send_message(uid, f"✅ Allowed user: {target}", reply_markup=admin_kb())
        else:
            bot.send_message(uid, f"❌ Failed to allow user: {target}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # DISALLOW USER STATE
    # ===============================================
    elif state == "disallow":
        USER_STATE.pop(uid, None)
        if not txt.isdigit():
            bot.send_message(uid, "❌ Invalid user ID. Must be digits only.")
            return True
        target = int(txt)
        if target == OWNER_ID:
            bot.send_message(uid, "⚠️ Cannot disallow the owner!")
            return True
        if disallow_user(target):
            bot.send_message(uid, f"✅ Disallowed user: {target}", reply_markup=admin_kb())
        else:
            bot.send_message(uid, f"❌ Failed to disallow user: {target}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # GIVE CREDIT STATE
    # ===============================================
    elif state == "give_credit":
        USER_STATE.pop(uid, None)
        parts = txt.split()
        if len(parts) != 3:
            bot.send_message(uid, "❌ Format: <user_id> <amount> <days>")
            return True
        try:
            target_id = int(parts[0])
            amount = int(parts[1])
            days = int(parts[2])
            if amount <= 0:
                bot.send_message(uid, "❌ Amount must be positive.")
                return True
            set_user_credits(target_id, amount, days)
            bot.send_message(uid, 
                           f"✅ Gave {amount} credits to user {target_id}\n"
                           f"Valid for: {days if days > 0 else '∞'} days",
                           reply_markup=admin_kb())
        except ValueError:
            bot.send_message(uid, "❌ Invalid format. Use numbers only.")
        return True
    
    # ===============================================
    # GENERATE REDEEM CODE STATE
    # ===============================================
    elif state == "gen_redeem":
        USER_STATE.pop(uid, None)
        parts = txt.split()
        if len(parts) != 2:
            bot.send_message(uid, "❌ Format: <amount> <days>")
            return True
        try:
            amount = int(parts[0])
            days = int(parts[1])
            if amount <= 0:
                bot.send_message(uid, "❌ Amount must be positive.")
                return True
            code = gen_redeem_code(amount, days, uid)
            bot.send_message(uid, 
                           f"✅ Redeem Code Generated!\n\n"
                           f"🔑 Code: `{code}`\n"
                           f"💰 Credits: {amount}\n"
                           f"⏱ Valid: {days if days > 0 else '∞'} days\n\n"
                           f"Share this code with users!",
                           parse_mode="Markdown",
                           reply_markup=admin_kb())
        except Exception as e:
            bot.send_message(uid, f"❌ Error: {str(e)}", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # SHOW CREDITS STATE
    # ===============================================
    elif state == "show_credits":
        USER_STATE.pop(uid, None)
        if txt.upper() == "ALL":
            try:
                cur.execute("SELECT user_id, credits, expires_at FROM user_credits WHERE credits > 0")
                rows = cur.fetchall()
                if not rows:
                    bot.send_message(uid, "📊 No users with credits.", reply_markup=admin_kb())
                    return True
                
                lines = ["📊 Users with Credits:\n"]
                for r in rows[:50]:
                    user_id, credits, expires = r
                    if expires:
                        exp_date = datetime.datetime.fromtimestamp(expires).strftime("%Y-%m-%d")
                        lines.append(f"👤 {user_id}: {credits} credits (expires: {exp_date})")
                    else:
                        lines.append(f"👤 {user_id}: {credits} credits (no expiry)")
                
                msg = "\n".join(lines)
                if len(rows) > 50:
                    msg += f"\n\n... and {len(rows) - 50} more users"
                bot.send_message(uid, msg, reply_markup=admin_kb())
            except Exception as e:
                bot.send_message(uid, f"❌ Error: {str(e)}", reply_markup=admin_kb())
        
        elif txt.isdigit():
            target = int(txt)
            credits, expires = get_user_credits(target)
            if expires:
                exp_date = datetime.datetime.fromtimestamp(expires).strftime("%Y-%m-%d %H:%M")
                msg = f"📊 User {target}:\n💰 Credits: {credits}\n⏱ Expires: {exp_date}"
            else:
                msg = f"📊 User {target}:\n💰 Credits: {credits}\n⏱ Expires: Never"
            bot.send_message(uid, msg, reply_markup=admin_kb())
        else:
            bot.send_message(uid, "❌ Invalid input. Send user ID or 'ALL'.", reply_markup=admin_kb())
        return True
    
    # ===============================================
    # BROADCAST STATE
    # ===============================================
    elif state == "broadcast":
        USER_STATE.pop(uid, None)
        if not txt:
            bot.send_message(uid, "❌ Message cannot be empty.", reply_markup=admin_kb())
            return True
        
        users = get_all_users()
        success = 0
        failed = 0
        
        status_msg = bot.send_message(uid, f"📣 Broadcasting to {len(users)} users...")
        
        for user_row in users:
            target_id = user_row[0]
            try:
                bot.send_message(target_id, f"📢 Broadcast Message:\n\n{txt}")
                success += 1
                time.sleep(0.05)  # Small delay to avoid rate limits
            except Exception:
                failed += 1
        
        try:
            bot.edit_message_text(
                f"✅ Broadcast Complete!\n\n"
                f"✅ Sent: {success}\n"
                f"❌ Failed: {failed}",
                uid,
                status_msg.message_id
            )
        except:
            pass
        
        bot.send_message(uid, "↩️ Returning to admin panel...", reply_markup=admin_kb())
        return True
    
    return False


# ===============================================
# MODULE INFO
# ===============================================

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ['admin_kb', 'require_owner', 'register_admin_handlers', 'process_admin_states']