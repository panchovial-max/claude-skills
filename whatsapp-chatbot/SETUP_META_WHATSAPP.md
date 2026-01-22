# Meta WhatsApp Business API Setup Guide

## Step 1: Create Meta Developer Account

1. Go to **https://developers.facebook.com**
2. Click "Get Started" or "Log In" (use your Facebook account)
3. Accept the Developer Terms

---

## Step 2: Create a Meta App

1. Go to **https://developers.facebook.com/apps/**
2. Click **"Create App"**
3. Select **"Business"** as the app type
4. Fill in:
   - **App name:** `PVB WhatsApp Bot`
   - **App contact email:** your email
   - **Business Account:** Create one or select existing
5. Click **"Create App"**

---

## Step 3: Add WhatsApp Product

1. In your new app dashboard, scroll to **"Add Products"**
2. Find **"WhatsApp"** and click **"Set Up"**
3. You'll be taken to WhatsApp > Getting Started

---

## Step 4: Get Your Credentials

### A. Phone Number ID
1. In **WhatsApp > Getting Started**
2. Under "From" dropdown, you'll see a test phone number
3. Click **"Manage phone numbers"** or look for **Phone Number ID**
4. Copy the **Phone Number ID** (looks like: `123456789012345`)

### B. Business Account ID
1. Look at the URL in your browser
2. Find `business_id=XXXXX` in the URL
3. Or go to **WhatsApp > Configuration** and find it there
4. Copy the **Business Account ID**

### C. Access Token (Temporary)
1. In **WhatsApp > Getting Started**
2. Under "Temporary access token" section
3. Click **"Generate"** or copy the existing token
4. Copy the **Access Token** (starts with `EAA...`)

**Note:** Temporary tokens expire in 24 hours. For production, you'll need a permanent token.

---

## Step 5: Create Verify Token

Create a random string to use as your verify token. This can be anything:

```
pvb_whatsapp_verify_2026
```

Or generate one:
```bash
openssl rand -hex 16
```

Save this - you'll use it in both your `.env` file and Meta webhook setup.

---

## Step 6: Your Credentials Summary

After completing steps above, you should have:

| Credential | Example | Where to find |
|------------|---------|---------------|
| `META_BUSINESS_ACCOUNT_ID` | `123456789012345` | URL or WhatsApp > Configuration |
| `META_PHONE_NUMBER_ID` | `109876543210987` | WhatsApp > Getting Started |
| `META_ACCESS_TOKEN` | `EAAGm0PX4ZCps...` | WhatsApp > Getting Started |
| `META_VERIFY_TOKEN` | `pvb_whatsapp_verify_2026` | You create this |

---

## Step 7: Configure Webhook (After Local Setup)

**Wait until your local server is running with ngrok!**

1. Go to **WhatsApp > Configuration**
2. Under **Webhook**, click **"Edit"**
3. Enter:
   - **Callback URL:** `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - **Verify Token:** Your `META_VERIFY_TOKEN` from `.env`
4. Click **"Verify and Save"**
5. Under **Webhook fields**, subscribe to:
   - `messages`
   - `messaging_postbacks` (optional)

---

## Step 8: Add Test Phone Number

To test the bot:

1. Go to **WhatsApp > Getting Started**
2. Under "To" field, click **"Add phone number"**
3. Add your personal WhatsApp number
4. You'll receive a verification code via WhatsApp
5. Enter the code to verify

**Note:** With a test number, you can only message numbers you've added here.

---

## Troubleshooting

### "Webhook verification failed"
- Check your `META_VERIFY_TOKEN` matches exactly in `.env` and Meta
- Make sure your server is running and accessible via ngrok
- Check the ngrok URL is correct and uses HTTPS

### "Access token expired"
- Temporary tokens expire in 24 hours
- Go back to Getting Started and generate a new one
- Update your `.env` file

### "Phone number not verified"
- Add your test number in WhatsApp > Getting Started
- Complete the verification process

### "Message not delivered"
- Check your Access Token is valid
- Verify the recipient number is in your allowed test numbers
- Check server logs for errors

---

## Next Steps

Once you have all credentials:

1. Create your `.env` file (see below)
2. Run the chatbot locally
3. Set up ngrok
4. Configure the webhook in Meta
5. Test by sending a message to the test number

---

## Quick Reference Links

- Meta Developers: https://developers.facebook.com
- WhatsApp Business Platform: https://business.whatsapp.com
- Cloud API Docs: https://developers.facebook.com/docs/whatsapp/cloud-api
- Webhook Reference: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks

---

*Last updated: January 2026*
