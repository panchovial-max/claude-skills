# PVB ChatBot - Quick Start for Pancho

## You now have a complete, customized WhatsApp chatbot! 🎉

This guide walks you through getting it live in minutes.

---

## What You Have

✅ **Complete chatbot system** that:
- Welcomes visitors from Instagram
- Routes them to Photography or Marketing
- Qualifies leads automatically
- Recommends the right service tier
- Notifies you immediately via n8n
- Stores all data in database

✅ **Configuration ready** with:
- Your exact service prices ($600, $1-3k, $3-7k)
- Your photography specialties (Ecuestre, Automotriz, Video)
- Your brand messaging
- Smart lead scoring
- Automated follow-ups

✅ **Complete documentation** including:
- Setup guide (SETUP.md)
- Deployment checklist (DEPLOYMENT_CHECKLIST.md)
- Services reference (SERVICES_REFERENCE.md)
- Architecture overview (ARCHITECTURE.md)

---

## 3 Quick Steps to Go Live

### Step 1: Environment Setup (5 minutes)
```bash
# In the whatsapp-chatbot folder:
cp .env.example .env
```

Then edit `.env` and add:
```
META_API_TOKEN=your_token_from_meta
META_PHONE_NUMBER_ID=your_phone_id
META_BUSINESS_ACCOUNT_ID=your_business_id
WEBHOOK_VERIFY_TOKEN=just_pick_any_random_string
N8N_WEBHOOK_URL=https://your-n8n-instance/webhook
DATABASE_URL=sqlite:///chatbot.db
```

### Step 2: Initialize Database (2 minutes)
```bash
python -c "from app.models.database import Base, engine; Base.metadata.create_all(engine)"
```

### Step 3: Deploy (5 minutes)
Choose one:

**Option A: Heroku** (simplest)
```bash
heroku create pvb-chatbot
heroku config:set META_API_TOKEN=xxx (repeat for each var in .env)
git push heroku main
```

**Option B: Railway** (recommended, free tier)
- Go to https://railway.app
- Connect your GitHub repo
- Add env variables
- Deploy automatically

**Option C: Your own server**
```bash
python -m flask run --host 0.0.0.0 --port 5000
```

---

## Configuration You Need from Meta

1. **Create Meta App**: https://developers.facebook.com
2. **Add WhatsApp Product**
3. **Get Phone Number** (verify a business number)
4. **Get API Token** (from App Settings)
5. **Set Webhook URL** to your deployed app: `https://your-app/webhook`
6. **Subscribe to webhook** to receive messages

---

## Setting Up Notifications (n8n)

You need n8n to get notified when leads come in:

1. **Deploy n8n** (self-hosted or cloud)
2. **Create a Webhook trigger**
3. **Create workflow**:
   - Receive webhook with lead data
   - Send email to pancho@pvbstudio.com
   - Send WhatsApp to your number
   - Create calendar event (optional)

---

## Test It Works

Once deployed, test by:

1. Send a message to your WhatsApp number
2. You should get the greeting with 4 options
3. Select "1" for photography
4. Complete the flow
5. Check n8n received the lead
6. Check database for stored lead

---

## What Happens When Someone Contacts You

### Via Instagram:
1. Person clicks WhatsApp in bio
2. Conversation starts with bot
3. Bot asks about their needs

### Photography Lead Example:
- Choose: "1️⃣ Fotografía"
- Bot asks: What type? (Ecuestre/Automotriz/Video)
- Bot asks: Context? (Gallery/Brand/Personal)
- Bot asks: Location, Date, Budget
- Bot collects: Name, Email, WhatsApp
- Bot says: "Pancho will contact you in 24-48 hours"
- **n8n notifies you immediately** ✅

### Marketing Lead Example:
- Choose: "2️⃣ Marketing"
- Bot asks: What's your problem?
- Bot asks: Current campaigns?
- Bot asks: Current spend?
- Bot recommends: AI Ads ($600) or Strategic ($1-3k) or Premium ($3-7k)
- Bot collects: Name, Company, Website, Email
- Bot says: "Pancho will call you for free consultation"
- **n8n notifies you immediately** ✅

### Quality Scoring:
- **HOT** 🔥: High budget + serious intent → Call immediately
- **WARM** 🟡: Medium interest → Call within 24h
- **COLD** ❄️: Just exploring → Email nurture

---

## Key Messages Customized for PVB

✅ **Greeting**: "Somos un estudio boutique que combina fotografía fine art con marketing digital potenciado por IA."

✅ **Photography**: "Fotografía de nivel galería especializada en ecuestre y automotriz"

✅ **Marketing**: "AI marketing con enfoque en resultados medibles y automatización"

✅ **Portfolio**: panchovial.com (automatically shared)

✅ **Services**: 
- Photography: Custom quotes from $1k
- Marketing: $600, $1-3k, $3-7k tiers

---

## File Structure Reference

```
whatsapp-chatbot/
├── app/
│   ├── config/
│   │   └── pvb_services.py      ← ALL messages & config here
│   ├── flows/
│   │   └── conversation_engine.py ← Conversation logic
│   ├── models/
│   │   └── database.py
│   ├── utils/
│   │   ├── meta_api.py
│   │   └── lead_router.py       ← Lead scoring
│   └── main.py                  ← Flask app
├── CUSTOMIZATION_SUMMARY.md     ← What changed
├── SERVICES_REFERENCE.md        ← Service details
├── DEPLOYMENT_CHECKLIST.md      ← Go live guide
├── SETUP.md                     ← Detailed setup
└── README_CUSTOMIZED.md         ← System overview
```

---

## Need to Change Something?

### Change a service price?
Edit `app/config/pvb_services.py` → Find the SERVICES dict → Update price

### Change greeting message?
Edit `app/config/pvb_services.py` → WELCOME_MESSAGE_ES

### Change marketing tiers?
Edit `app/config/pvb_services.py` → MARKETING_RECOMMENDATION_* vars

### Change lead scoring?
Edit `app/utils/lead_router.py` → LEAD_SCORING_WEIGHTS

### Add a new FAQ?
Edit `app/config/pvb_services.py` → FAQS dict

All changes take effect immediately (on next message).

---

## Success Metrics (First Month)

Track these to know it's working:

📊 **Capture Rate**
- Incoming messages
- Leads completed conversation
- Lead completion rate (target: >70%)

💰 **Lead Quality**
- % HOT leads (high budget/intent)
- % WARM leads
- % COLD leads

📱 **Service Distribution**
- Photography leads
- Marketing leads
- About/Info only

✉️ **Notifications**
- n8n webhooks received
- Email sent to you
- WhatsApp alerts

💬 **Engagement**
- Average conversation length
- Most popular service choice
- Questions asked in handoff

---

## Common Questions

**Q: Where do leads come from?**
A: Instagram bio link → WhatsApp → Chatbot. You can also share your WhatsApp number directly.

**Q: Can I change the messages?**
A: Yes! Edit `app/config/pvb_services.py` for all messages. No coding needed.

**Q: How does n8n know to notify me?**
A: When bot captures a lead, it sends lead data to your n8n webhook. You create the workflow there.

**Q: What if the bot doesn't understand someone?**
A: It asks them to choose again from the options. If they don't answer, you can manually follow up.

**Q: Can I test without deploying?**
A: Yes! Run `python -m flask run` locally, then test with Postman or curl.

**Q: How much does it cost?**
A: 
- WhatsApp: Free for first 1,000 messages/month, then $0.05-0.07/msg
- Hosting: Free (Heroku/Railway free tier)
- n8n: Free (self-hosted) or $10-50/month (cloud)
- Total: **Free to start, $0-60/month at scale**

---

## Next Steps

1. **Copy and save `.env.example` to `.env`**
   - Get values from Meta App dashboard
   - Get n8n webhook URL
   
2. **Follow DEPLOYMENT_CHECKLIST.md**
   - Has step-by-step for Heroku, Railway, AWS, etc.
   
3. **Set up n8n**
   - Create webhook for notifications
   - Test it receives data
   
4. **Update Meta Webhook**
   - Point to your deployed app
   - Verify connection
   
5. **Add WhatsApp to Instagram**
   - Add link in bio: https://wa.me/your-number
   - Start promoting

6. **Monitor First Week**
   - Check incoming messages
   - Verify leads being scored correctly
   - Make sure you get notifications

---

## Support & Documentation

📖 **DEPLOYMENT_CHECKLIST.md** - Complete pre/post deployment guide
📖 **SERVICES_REFERENCE.md** - All service details & messaging
📖 **SETUP.md** - Detailed 30-min setup guide with screenshots
📖 **ARCHITECTURE.md** - How the system works
📖 **CUSTOMIZATION_SUMMARY.md** - What was customized for you
📖 **README_CUSTOMIZED.md** - System overview

---

## You're Ready! 🚀

Your chatbot is:
- ✅ Fully customized for PVB services
- ✅ Configured with exact prices
- ✅ Ready to capture qualified leads
- ✅ Set up to notify you automatically
- ✅ Documented for easy updates

**Next action**: Follow DEPLOYMENT_CHECKLIST.md to go live!

Questions? Review the docs above or contact me for technical support.

---

**Made with ❤️ for PVB Estudio Creativo**
