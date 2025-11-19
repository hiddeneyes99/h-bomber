# 🚀 Complete Render Deployment Guide for Telegram Bot

This guide will help you deploy your **ULTRA BOMBER 3000+** Telegram bot to Render with PostgreSQL database for production use.

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ A GitHub account
- ✅ A Render account (free tier available at https://render.com)
- ✅ Your Telegram Bot Token
- ✅ This code pushed to a GitHub repository

---

## 🎯 Step-by-Step Deployment Process

### Step 1: Push Your Code to GitHub

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name your repository (e.g., `telegram-bomber-bot`)
   - Make it **Private** (recommended for bots)
   - Don't initialize with README (you already have code)

2. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

---

### Step 2: Create PostgreSQL Database on Render

1. **Go to Render Dashboard:**
   - Visit https://dashboard.render.com
   - Click **"New +"** button (top right)
   - Select **"PostgreSQL"**

2. **Configure the database:**
   - **Name:** `telegram-bot-db` (or any name you want)
   - **Database:** `bomber_db` (will be created automatically)
   - **User:** `bomber_user` (will be created automatically)
   - **Region:** Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version:** Latest (15 or 16)
   - **Plan:** **Free** (sufficient for your bot)

3. **Create Database:**
   - Click **"Create Database"**
   - Wait 2-3 minutes for database to be provisioned
   - ✅ Database will be created and you'll see the dashboard

4. **Copy Database Connection Info:**
   - On the database page, you'll see **"Connections"** section
   - Find **"Internal Database URL"** (starts with `postgresql://`)
   - **Copy this URL** - you'll need it in Step 4
   - Example: `postgresql://bomber_user:xxxxx@dpg-xxxxx/bomber_db`

---

### Step 3: Create Background Worker on Render

1. **Create New Web Service:**
   - Go back to Render Dashboard
   - Click **"New +"** button
   - Select **"Background Worker"** (NOT Web Service!)
   - **Why Background Worker?** Your bot doesn't need HTTP ports, it just runs continuously

2. **Connect to GitHub:**
   - Click **"Connect account"** if this is your first time
   - Select your repository from the list
   - Click **"Connect"**

3. **Configure the Service:**

   **Basic Settings:**
   - **Name:** `telegram-bomber-bot` (any name)
   - **Region:** Same as your database (e.g., `Oregon (US West)`)
   - **Branch:** `main`
   - **Root Directory:** Leave empty (unless code is in subfolder)

   **Build & Deploy:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

   **Plan:**
   - Select **"Free"** plan (sufficient for your bot)

---

### Step 4: Add Environment Variables

This is the most important step! Your bot needs these variables to work.

1. **Click "Advanced" or scroll down to "Environment Variables"**

2. **Add these environment variables one by one:**

   | Key | Value | Description |
   |-----|-------|-------------|
   | `DATABASE_URL` | Paste the Internal Database URL from Step 2 | PostgreSQL connection string |
   | `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Required for bot to work |
   | `CHANNEL_USERNAME` | `@technicalwhitehat` | Your channel username |
   | `BOT_NAME` | `ULTRA BOMBER 3000+` | Your bot's display name |

   **Example:**
   ```
   Key: DATABASE_URL
   Value: postgresql://bomber_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com/bomber_db

   Key: TELEGRAM_BOT_TOKEN
   Value: 8545605385:AAEPBwsoxJ390NEXXyK6fpjlLGL9fc2rVAM

   Key: CHANNEL_USERNAME
   Value: @technicalwhitehat

   Key: BOT_NAME
   Value: ULTRA BOMBER 3000+
   ```

3. **Save Environment Variables:**
   - Make sure all 4 variables are added
   - Double-check DATABASE_URL is correct

---

### Step 5: Deploy Your Bot

1. **Create Service:**
   - Scroll down and click **"Create Background Worker"**
   - Render will start building your bot

2. **Monitor the Build:**
   - You'll see build logs in real-time
   - Build takes 1-3 minutes
   - Look for these success messages:
     ```
     Successfully installed packages
     ==> Starting service with 'python bot.py'
     🗄️ Using PostgreSQL database
     🤖 ULTRA BOMBER 3000+ Telegram Bot Started!
     ```

3. **Check Status:**
   - Service should show **"Live"** status (green)
   - If it shows "Build Failed" or "Deploy Failed", check the logs

---

## ✅ Verification Steps

After deployment, verify everything works:

### 1. Check Logs
- On Render dashboard, click on your bot service
- Click **"Logs"** tab
- You should see:
  ```
  🗄️ Using PostgreSQL database
  🤖 ULTRA BOMBER 3000+ Telegram Bot Started!
  📢 Force join enabled for: @technicalwhitehat
  💣 Loaded 116 ULTRA FAST APIs
  ```

### 2. Test on Telegram
- Open Telegram
- Search for your bot
- Send `/start` command
- Bot should respond with welcome message
- New user should get 1500 free credits

### 3. Test Database Persistence
- Send `/start` to your bot
- Check your credits with "💰 My Credits" button
- Stop and restart the service on Render:
  - Go to your service → Click "Manual Deploy" → "Clear build cache & deploy"
- After restart, send `/start` again
- Your credits should still be there! ✅

---

## 🔧 Troubleshooting

### Problem: Bot doesn't start (Build Failed)

**Solution:**
1. Check build logs for errors
2. Make sure `requirements.txt` is correct
3. Verify Python version is compatible

### Problem: Bot starts but doesn't respond

**Solution:**
1. Check if `TELEGRAM_BOT_TOKEN` environment variable is correct
2. Make sure your bot token is active (test with @BotFather)
3. Check logs for error messages

### Problem: Database connection error

**Solution:**
1. Verify `DATABASE_URL` is copied correctly (no extra spaces)
2. Make sure database is in "Available" state on Render
3. Check database and bot are in the same region
4. Copy the **Internal Database URL**, not External

### Problem: Credits/data disappear after restart

**Solution:**
1. Check logs - you should see "🗄️ Using PostgreSQL database"
2. If you see "🗄️ Using SQLite database", then DATABASE_URL is not set correctly
3. Verify DATABASE_URL environment variable exists and is correct

### Problem: Free tier limitations

**Render Free Tier Limits:**
- Background Worker sleeps after 15 minutes of inactivity
- 750 hours/month free (enough for one bot running 24/7)
- Database: 1GB storage, 97 hours/month free

**Solutions:**
- Use cron-job.org or UptimeRobot to ping your bot every 14 minutes (keeps it awake)
- Upgrade to paid plan ($7/month) for always-on service

---

## 🎨 Advanced Configuration

### Auto-Deploy on Git Push

Render automatically deploys when you push to GitHub:
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Updated bot features"
   git push origin main
   ```
3. Render will automatically rebuild and deploy your bot

### View and Manage Database

1. On Render dashboard, go to your PostgreSQL database
2. Click **"Connect"** → Copy PSQL command
3. Use any PostgreSQL client (like pgAdmin, DBeaver) to connect
4. Or use Render's built-in **"Shell"** tab to run SQL commands

### Environment-Specific Settings

Your code automatically detects the environment:
- **On Replit:** Uses SQLite (bomber_users.db file)
- **On Render:** Uses PostgreSQL (DATABASE_URL is present)
- **No code changes needed!**

---

## 📊 Monitoring Your Bot

### Check Logs
```
Render Dashboard → Your Service → Logs tab
```

### Monitor Database Usage
```
Render Dashboard → Your Database → Metrics tab
```

### View User Activity
You can see all user data in PostgreSQL:
```sql
SELECT * FROM users ORDER BY join_date DESC;
SELECT * FROM credits;
SELECT * FROM attacks ORDER BY timestamp DESC LIMIT 50;
```

---

## 💡 Best Practices

1. **Keep Secrets Secret:**
   - Never commit bot tokens to GitHub
   - Always use environment variables

2. **Regular Backups:**
   - Render Free tier doesn't include automated backups
   - Manually export database periodically

3. **Monitor Logs:**
   - Check logs daily for errors
   - Set up email notifications in Render settings

4. **Update Dependencies:**
   - Keep `requirements.txt` updated
   - Test updates locally before deploying

---

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Render Docs:** https://render.com/docs
- **PostgreSQL on Render:** https://render.com/docs/databases
- **Background Workers:** https://render.com/docs/background-workers

---

## ✨ Success Checklist

Before closing this guide, make sure:

- ✅ Code is pushed to GitHub
- ✅ PostgreSQL database is created on Render
- ✅ Background Worker is deployed and showing "Live" status
- ✅ All 4 environment variables are set correctly
- ✅ Bot responds to `/start` on Telegram
- ✅ Credits persist after restart (database working)
- ✅ Logs show "Using PostgreSQL database"

---

## 🎉 Congratulations!

Your Telegram bot is now running in production on Render with a persistent PostgreSQL database!

**Your users will now:**
- Get 1500 free credits on signup ✅
- Keep their credits even after server restarts ✅
- Have their attack history saved permanently ✅

**Questions?** Contact: @technicalwhitehat
