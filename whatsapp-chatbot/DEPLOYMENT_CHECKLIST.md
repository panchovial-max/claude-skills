# PVB Chatbot - Deployment Checklist

## Pre-Deployment (Before Going Live)

### 1. Environment Configuration
- [ ] Create `.env` file from `.env.example`
- [ ] Add `META_API_TOKEN` from Meta App
- [ ] Add `META_PHONE_NUMBER_ID` from WhatsApp Business Account
- [ ] Add `META_BUSINESS_ACCOUNT_ID`
- [ ] Add `WEBHOOK_VERIFY_TOKEN` (generate random string)
- [ ] Add database URL (SQLite for dev, PostgreSQL for prod)
- [ ] Add `N8N_WEBHOOK_URL` for lead notifications
- [ ] Add Pancho's contact info (optional)

### 2. Database Setup
- [ ] Initialize database: `python -c "from app.models.database import Base, engine; Base.metadata.create_all(engine)"`
- [ ] Verify database file created
- [ ] Test database connection

### 3. Meta App Configuration
- [ ] Create Facebook App: https://developers.facebook.com
- [ ] Add WhatsApp Product
- [ ] Create WhatsApp Business Account
- [ ] Get Phone Number (verified)
- [ ] Generate API Token
- [ ] Set webhook URL in Meta App dashboard
- [ ] Verify webhook works (should see Meta verification in logs)

### 4. Conversation Testing (Local)
- [ ] Start Flask app: `python -m flask run`
- [ ] Test greeting flow locally
- [ ] Test photography flow
- [ ] Test marketing flow
- [ ] Test about/info flow
- [ ] Verify all messages display correctly
- [ ] Check database logging of conversations
- [ ] Verify lead scoring logic

### 5. n8n Setup
- [ ] Deploy n8n instance (self-hosted or cloud)
- [ ] Create webhook trigger
- [ ] Test incoming webhook
- [ ] Create email notification workflow
- [ ] Create WhatsApp notification to Pancho
- [ ] Test full workflow end-to-end

### 6. Code Review
- [ ] Verify all service prices are correct ($600, $1-3k, $3-7k)
- [ ] Check all messaging matches brand voice
- [ ] Verify photography budget ranges
- [ ] Confirm FAQ responses are accurate
- [ ] Test lead quality scoring weights
- [ ] Check error handling for API failures

---

## Deployment (Choose Your Platform)

### Option A: Heroku (Simplest)
- [ ] Install Heroku CLI
- [ ] Create Heroku app: `heroku create pvb-chatbot`
- [ ] Set environment variables:
  ```bash
  heroku config:set META_API_TOKEN=xxx
  heroku config:set META_PHONE_NUMBER_ID=xxx
  heroku config:set N8N_WEBHOOK_URL=xxx
  # ... etc
  ```
- [ ] Push code: `git push heroku main`
- [ ] Initialize database: `heroku run python -c "from app.models.database import Base, engine; Base.metadata.create_all(engine)"`
- [ ] View logs: `heroku logs -t`
- [ ] Update Meta webhook URL to: `https://pvb-chatbot.herokuapp.com/webhook`

### Option B: Railway (Recommended)
- [ ] Create Railway account: https://railway.app
- [ ] Connect GitHub repo
- [ ] Add environment variables in Railway dashboard
- [ ] Deploy automatic on push
- [ ] Database (Railway PostgreSQL) auto-created
- [ ] Update Meta webhook URL to Railway deployment URL

### Option C: AWS Lambda + API Gateway
- [ ] Create Lambda function (Python 3.9+)
- [ ] Upload app code as zip
- [ ] Create API Gateway endpoint
- [ ] Add environment variables via Lambda console
- [ ] Create RDS PostgreSQL database
- [ ] Point Meta webhook to API Gateway URL

### Option D: DigitalOcean App Platform
- [ ] Create DigitalOcean account
- [ ] Create new App from GitHub
- [ ] Configure environment variables
- [ ] Enable HTTPS (automatic)
- [ ] Create PostgreSQL database
- [ ] Deploy

---

## Post-Deployment Testing

### 1. Webhook Verification
- [ ] Meta shows "Active" status for webhook
- [ ] Check app logs for incoming test messages
- [ ] Verify signature verification passes

### 2. End-to-End Flow Testing (via WhatsApp)
- [ ] Send "Hola" to bot WhatsApp number
- [ ] Receive greeting with 4 options
- [ ] Test each option (1, 2, 3, 4)
- [ ] Complete full photography flow
  - [ ] Project type selection
  - [ ] Context selection
  - [ ] Location entry
  - [ ] Date entry
  - [ ] Budget selection
  - [ ] Confirmation message
- [ ] Complete full marketing flow
  - [ ] Problem selection
  - [ ] Campaign history
  - [ ] Current spend
  - [ ] Budget recommendation
  - [ ] Confirmation message
- [ ] Test "About" flow
- [ ] Test direct handoff to Pancho

### 3. Lead Capture Verification
- [ ] Check database for captured leads
- [ ] Verify all fields populated correctly
- [ ] Check lead quality scoring (HOT/WARM/COLD)
- [ ] Verify service recommendations

### 4. Notification Testing
- [ ] Complete a photography lead capture
- [ ] Verify n8n receives webhook
- [ ] Verify Pancho gets email notification
- [ ] Verify Pancho gets WhatsApp notification
- [ ] Complete a marketing lead capture
- [ ] Verify correct tier recommendation sent

### 5. Message Quality Check
- [ ] All emojis display correctly
- [ ] Line breaks format properly
- [ ] Quick replies show as buttons
- [ ] No encoding issues with Spanish characters

---

## Instagram Integration

### 1. Set Up Lead Ads (Optional)
- [ ] Create Facebook Page for PVB Studio
- [ ] Add Instagram account to Page
- [ ] Create lead ad campaign
- [ ] Add WhatsApp CTA
- [ ] Configure click destination to WhatsApp link

### 2. WhatsApp Link Setup
- [ ] Get WhatsApp Business account URL
- [ ] Add to Instagram bio: https://wa.me/your-number?text=Hola
- [ ] Add to TikTok profile
- [ ] Add to YouTube descriptions

### 3. Web Integration (Optional)
- [ ] Add WhatsApp chat widget to website
- [ ] Use Twilio SDK or Meta SDK
- [ ] Track attribution to web visitors

---

## Post-Live Monitoring (Week 1-2)

### Daily Checks
- [ ] Monitor incoming message volume
- [ ] Check for any error logs
- [ ] Verify Pancho receiving notifications
- [ ] Monitor n8n webhook performance
- [ ] Check database growth

### Weekly Report
- [ ] Total leads captured
- [ ] Lead quality breakdown
- [ ] Average conversation length
- [ ] Conversion rate (from Instagram → WhatsApp → Lead)
- [ ] Most popular service choice
- [ ] Any error patterns

### Performance Optimization
- [ ] Review slow responses
- [ ] Check database query performance
- [ ] Optimize n8n workflows if needed
- [ ] Update messaging based on user feedback
- [ ] Track which questions cause drop-off

---

## Ongoing Maintenance

### Monthly Tasks
- [ ] Review and update service prices if needed
- [ ] Audit conversation quality
- [ ] Check API limits (Meta free tier = 1,000 msgs/month)
- [ ] Review lead quality scores
- [ ] Update FAQ if needed

### Quarterly Tasks
- [ ] Review total ROI
- [ ] A/B test different messaging
- [ ] Update portfolio link if needed
- [ ] Check for new Meta API features
- [ ] Scale n8n automation if needed

### Security & Compliance
- [ ] Keep dependencies updated
- [ ] Rotate API tokens regularly
- [ ] Monitor for suspicious activity
- [ ] Ensure GDPR compliance for EU leads
- [ ] Backup database regularly

---

## Troubleshooting Common Issues

### Issue: Webhook not receiving messages
**Check**:
- [ ] Webhook URL is correct in Meta App dashboard
- [ ] `WEBHOOK_VERIFY_TOKEN` matches in code
- [ ] Flask app is running and accessible
- [ ] No firewall blocking requests
- [ ] Check app logs for errors

### Issue: Leads not being stored in database
**Check**:
- [ ] Database connection string is correct
- [ ] Tables were created (`Base.metadata.create_all()`)
- [ ] No database errors in logs
- [ ] Verify conversation flow completes

### Issue: n8n not receiving notifications
**Check**:
- [ ] `N8N_WEBHOOK_URL` is correct in .env
- [ ] n8n webhook is active
- [ ] No firewall blocking outbound requests
- [ ] Check n8n logs for incoming requests

### Issue: Wrong service tier recommended
**Check**:
- [ ] Lead scoring weights in `pvb_services.py`
- [ ] Service tier thresholds
- [ ] User input being captured correctly
- [ ] Test with sample data

### Issue: Message formatting looks wrong
**Check**:
- [ ] WhatsApp message formatting in `pvb_services.py`
- [ ] Check for special characters or encoding
- [ ] Verify line breaks (\n) are working
- [ ] Test emoji compatibility

---

## Rollback Plan

If something breaks:
1. Stop receiving messages: Disable webhook in Meta App dashboard
2. Revert code: `git revert [commit-hash]` and redeploy
3. Check logs for error: `heroku logs -t` or equivalent
4. Fix issue and redeploy
5. Re-enable webhook once working

---

## Success Criteria (After 1 Month)

✅ **Technical**:
- 0 unhandled errors in logs
- 100% webhook uptime
- <2 second response time per message
- Database growing as expected

✅ **Business**:
- 50+ leads captured
- 80%+ conversation completion rate
- 20%+ are HOT quality leads
- 0 customer complaints about chatbot

✅ **Next Optimization**:
- A/B test different greetings
- Add FAQ section for top questions
- Integrate with CRM for better tracking
- Scale marketing spend on ads that work

---

**Need Help?**
- Check SETUP.md for detailed configuration
- Review ARCHITECTURE.md for system overview
- See CONVERSATION_EXAMPLES.md for real examples
- Contact Pancho for business-related questions
