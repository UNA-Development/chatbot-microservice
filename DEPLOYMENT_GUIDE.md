# Chatbot Deployment Guide

## ✅ Backend Deployed!

The chatbot backend API is now live on Vercel:

**API URL**: `https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app`

## What's Next: Adding the Widget to Your Websites

Your lead developer needs to add the chatbot widget to both websites. It's super simple - just add a few lines of code.

---

## For Rx4Miracles Website (rx4miracles.org)

Add this code **before the closing `</body>` tag** on every page where you want the chatbot:

```html
<!-- Chatbot Widget -->
<link rel="stylesheet" href="https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app/chatbot.css">
<div id="rx4m-chatbot-container"></div>
<script src="https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app/chatbot.js"></script>
<script>
    RX4MChatbot.init({
        apiUrl: 'https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app',
        site: 'rx4miracles',
        position: 'bottom-right'
    });
</script>
```

---

## For Louisiana Dental Plan Website (louisianadentalplan.com)

Add this code **before the closing `</body>` tag** on every page where you want the chatbot:

```html
<!-- Chatbot Widget -->
<link rel="stylesheet" href="https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app/chatbot.css">
<div id="rx4m-chatbot-container"></div>
<script src="https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app/chatbot.js"></script>
<script>
    RX4MChatbot.init({
        apiUrl: 'https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app',
        site: 'louisianadental',
        position: 'bottom-right'
    });
</script>
```

**Notice**: The only difference is `site: 'louisianadental'` instead of `site: 'rx4miracles'`. This tells the widget which chatbot to use.

---

## Widget Customization Options

You can customize the chatbot position by changing the `position` parameter:

- `'bottom-right'` (default) - Bottom right corner
- `'bottom-left'` - Bottom left corner

Example:
```javascript
RX4MChatbot.init({
    apiUrl: 'https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app',
    site: 'rx4miracles',
    position: 'bottom-left'  // Changed position
});
```

---

## Testing the Widget

After adding the code:

1. **Open your website in a browser**
2. **Look for the chat bubble** in the bottom right (or left) corner
3. **Click it** to open the chat
4. **Ask a question** like "What pharmacies accept this card?"
5. **Verify the greeting message** is correct:
   - Rx4Miracles: "Hey! I'm here to help you save on prescriptions with Rx4Miracles. How can I assist you today?"
   - Louisiana Dental: "Welcome to Louisiana Dental Plan! How can we help you today?"

---

## Hosting Widget Files (Alternative Option)

If you prefer to host the widget files (`chatbot.js` and `chatbot.css`) on your own server instead of loading them from Vercel:

1. **Copy files** from the GitHub repo:
   - `widget/chatbot.js`
   - `widget/chatbot.css`

2. **Upload to your web server** (e.g., `/assets/js/chatbot.js` and `/assets/css/chatbot.css`)

3. **Update the HTML** to reference your local files:

```html
<!-- Chatbot Widget -->
<link rel="stylesheet" href="/assets/css/chatbot.css">
<div id="rx4m-chatbot-container"></div>
<script src="/assets/js/chatbot.js"></script>
<script>
    RX4MChatbot.init({
        apiUrl: 'https://rx4m-chatbot-pknq32lp4-benpaulbooth-1822s-projects.vercel.app',
        site: 'rx4miracles',
        position: 'bottom-right'
    });
</script>
```

**Note**: The `apiUrl` should always point to the Vercel deployment, regardless of where you host the widget files.

---

## Updating the Chatbot Content

When you need to update the chatbot's knowledge or responses:

1. **Edit the knowledge files**:
   - `content/rx4miracles/knowledge.md`
   - `content/louisianadental/knowledge.md`

2. **Recreate the assistants**:
   ```bash
   cd backend
   python setup_assistants.py
   ```

3. **Update `.env` file** with new assistant IDs (the script will output them)

4. **Redeploy to Vercel**:
   ```bash
   vercel --prod --yes
   ```

5. **No website changes needed!** The chatbot will automatically use the updated knowledge.

---

## GitHub Repository

- **Repo**: https://github.com/benpbooth/rx4miracles-ldp-customer-service
- **Branch**: `main`
- All widget files are in the `/widget` directory

---

## Support & Troubleshooting

### Chatbot not appearing?
- Check browser console (F12) for JavaScript errors
- Verify the `<div id="rx4m-chatbot-container"></div>` exists
- Make sure scripts are loading (check Network tab)

### Getting errors when clicking chat button?
- Verify the API URL is correct
- Check that `site` parameter matches ('rx4miracles' or 'louisianadental')
- Open browser console to see error messages

### Widget showing wrong greeting?
- Double-check the `site` parameter in the init script
- Verify you're using the correct code snippet for each website

---

## Cost & Monitoring

- **Vercel Hosting**: Free tier (sufficient for current traffic)
- **OpenAI API**: ~$0.01 per conversation (pay as you go)
- **Estimated Monthly Cost**: ~$10-20 depending on chat volume

You can monitor API usage in the Vercel dashboard:
https://vercel.com/benpaulbooth-1822s-projects/rx4m-chatbot

---

## Questions?

Contact Ben or check the GitHub repo for more details!
