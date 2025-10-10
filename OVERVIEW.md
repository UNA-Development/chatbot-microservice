# Widget Integration Guide

## Overview
Widget files are served from your Heroku backend after deployment.

## Step 1: Deploy to Heroku
Follow [DEPLOYMENT.md](DEPLOYMENT.md) to deploy the backend.

Your deployment URL: `https://your-chatbot-api.herokuapp.com`

## Step 2: Add Widget to Louisiana Dental Plan

Add this code before the closing `</body>` tag:

```html
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://your-chatbot-api.herokuapp.com/widget/chatbot.css">
<script src="https://your-chatbot-api.herokuapp.com/widget/chatbot.js"></script>
<script>
  ChatbotWidget.init({
    apiUrl: 'https://your-chatbot-api.herokuapp.com',
    site: 'louisianadental'
  });
</script>
```

Replace `your-chatbot-api` with your actual Heroku app name.

## Step 3: Add Widget to Rx4Miracles

Add this code before the closing `</body>` tag:

```html
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://your-chatbot-api.herokuapp.com/widget/chatbot.css">
<script src="https://your-chatbot-api.herokuapp.com/widget/chatbot.js"></script>
<script>
  ChatbotWidget.init({
    apiUrl: 'https://your-chatbot-api.herokuapp.com',
    site: 'rx4miracles'
  });
</script>
```

Replace `your-chatbot-api` with your actual Heroku app name.

## What Happens

Louisiana Dental Plan:
- Green button (#2c5f2d)
- Greeting: "Welcome to Louisiana Dental Plan! How can we help you today?"
- Knows about dental plans, pricing, hours, providers

Rx4Miracles:
- Blue button (#0066cc)
- Greeting: "Hey! I'm here to help you save on prescriptions with Rx4Miracles..."
- Knows about prescription savings, pharmacies, free card program

Same widget code, different `site` parameter.

## Testing

Test on staging first:
1. Add widget code to staging site
2. Open in browser
3. Click chat button
4. Ask test questions

Expected behavior:
- Button appears in 1-2 seconds
- Opens on click
- Greeting appears
- Responds to messages

## Troubleshooting

Widget doesn't appear:
- Check browser console (F12)
- Verify Heroku app is running: `heroku ps`
- Check URLs for typos
- Verify `site` parameter matches database

Wrong colors/greeting:
- Check `site` parameter
- Louisiana Dental = `louisianadental`
- Rx4Miracles = `rx4miracles`

No response:
- Check logs: `heroku logs --tail`
- Verify API key: `heroku config:get OPENAI_API_KEY`
- Check assistant_id exists in database

## Customization

Change position:
```javascript
ChatbotWidget.init({
  apiUrl: 'https://your-chatbot-api.herokuapp.com',
  site: 'louisianadental',
  position: 'bottom-left'
});
```

## Adding More Companies

No redeployment needed:
1. Add via API
2. Create assistant: `heroku run python backend/setup_assistants.py`
3. Add widget with new `site_id`

Example:
```javascript
ChatbotWidget.init({
  apiUrl: 'https://your-chatbot-api.herokuapp.com',
  site: 'newcompany'
});
```
