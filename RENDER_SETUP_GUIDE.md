# 🚀 Render Web Service Deployment Guide

## Render pe Web Service Setup (Step-by-Step)

### Step 1: GitHub pe Code Push karo
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Render Dashboard pe jao
1. [Render.com](https://render.com) pe login karo
2. "New +" button pe click karo
3. **"Web Service"** select karo

### Step 3: Repository Connect karo
1. GitHub se apna repository select karo
2. Branch: `main` select karo

### Step 4: Configuration Settings
```
Name: ultra-bomber-bot (kuch bhi naam de sakte ho)
Region: Singapore (ya closest region)
Branch: main
Root Directory: (blank rakhna hai)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python web_server.py
```

### Step 5: Environment Variables Add karo
**Environment** section me ye add karo:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | Apna bot token yaha paste karo |
| `CHANNEL_USERNAME` | @technicalwhitehat (ya apna channel) |
| `BOT_NAME` | ULTRA BOMBER 3000+ |
| `DATABASE_URL` | (Agar PostgreSQL use kar rahe ho) |

### Step 6: Instance Type Select karo
- **Free Instance** select karo
- RAM: 512 MB (free tier)
- ⚠️ Free tier 15 minutes inactivity ke baad sleep mode me chala jata hai

### Step 7: Deploy karo
- "Create Web Service" button pe click karo
- Build process start hoga (2-3 minute lagega)
- Deploy successful hone ke baad URL mil jayega

## 🔄 24/7 Running ke liye (Free Solution)

Render free tier 15 minutes inactivity ke baad sleep hota hai. Ise active rakhne ke liye:

### Option 1: UptimeRobot (Recommended)
1. [UptimeRobot.com](https://uptimerobot.com) pe free account banao
2. "Add New Monitor" pe click karo
3. Monitor Type: **HTTP(s)**
4. URL: Apna Render web service URL (`https://your-app.onrender.com`)
5. Monitoring Interval: **5 minutes**
6. Save karo

Ye har 5 minute me tumhare app ko ping karega aur wo active rahega!

### Option 2: Cron-Job.org
1. [Cron-Job.org](https://cron-job.org) pe account banao
2. New Cronjob create karo
3. URL: Apna Render URL
4. Execution: Every 5 minutes
5. Save karo

### Option 3: Self-Ping (Code me)
Bot khud ko ping kar sakta hai (already handled in web_server.py)

## ✅ Verify Karo Bot Chal Raha Hai

1. Render dashboard me "Logs" tab check karo
2. Ye messages dikhai dene chahiye:
```
🤖 ULTRA BOMBER 3000+ Telegram Bot Started!
💣 Loaded 116 ULTRA FAST APIs
👑 Admin mode activated
```

3. Telegram pe apne bot ko `/start` command bhejo
4. Agar reply aata hai to **SUCCESS!** 🎉

## 🐛 Common Issues & Solutions

### Issue 1: Python 3.13 Error
**Error:** `AttributeError: 'Updater' object has no attribute...`
**Solution:** `runtime.txt` file already hai with Python 3.11.9 ✅

### Issue 2: Port Binding Error
**Error:** `Error: Port binding failed`
**Solution:** `web_server.py` already configured hai with PORT env variable ✅

### Issue 3: Bot Sleeping
**Solution:** UptimeRobot ya Cron-Job.org use karo (upar dekho)

### Issue 4: Database Connection Error
**Solution:** 
- Render dashboard me PostgreSQL database add karo (free tier available)
- Ya `.env` me SQLite use karne ke liye DATABASE_URL ko blank chod do

## 📝 Important Notes

- ✅ **runtime.txt** - Python 3.11.9 specify karta hai
- ✅ **Procfile** - Start command define karta hai
- ✅ **web_server.py** - Health check endpoint + bot running
- ✅ **requirements.txt** - Sabhi dependencies

## 🎯 Bot Features

- ⚡ 116+ Ultra Fast APIs
- 📞 Voice Call Bombing
- 📱 WhatsApp Bombing  
- 💬 SMS Bombing
- 👑 Admin Panel
- 💰 Credit System
- 🔐 Protected Numbers

## 🆘 Help Needed?

Agar koi issue aaye to:
1. Render logs check karo
2. Environment variables verify karo
3. Bot token correct hai ya nahi check karo

---
**Made with ❤️ by Technical White Hat**
