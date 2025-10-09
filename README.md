# RX4M Chatbot

AI-powered chat support for RX4 Miracles and Louisiana Dental Plan websites.

## Features

- 🤖 OpenAI GPT-4 powered conversations
- 🎨 Customizable widget for each site
- 📱 Mobile responsive design
- 💬 SMS support (coming soon)
- 🔒 CORS-protected API
- ⚡ Lightweight and fast

## Project Structure

```
rx4m-chatbot/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt     # Python dependencies
├── widget/
│   ├── chatbot.html         # Demo page
│   ├── chatbot.js           # Widget JavaScript
│   └── chatbot.css          # Widget styles
├── config/
│   ├── rx4miracles.yaml     # RX4 Miracles config
│   └── louisianadental.yaml # Louisiana Dental config
├── .env.example             # Environment variables template
└── README.md
```

## Quick Start

### 1. Set Up Backend

```bash
# Navigate to project
cd rx4m-chatbot

# Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cd ..
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Run Development Server

```bash
cd backend
source venv/bin/activate
python main.py
```

Server will start at `http://localhost:8000`

API docs available at `http://localhost:8000/docs`

### 3. Test the Widget

Open `widget/chatbot.html` in your browser to see the demo.

## Widget Integration

Your lead dev can integrate the widget by adding these lines to the website:

### For RX4 Miracles (rx4miracles.org):

```html
<!-- Add before closing </body> tag -->
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://your-cdn.com/chatbot.css">
<script src="https://your-cdn.com/chatbot.js"></script>
<script>
  RX4MChatbot.init({
    apiUrl: 'https://your-api-domain.com',
    site: 'rx4miracles',
    position: 'bottom-right'
  });
</script>
```

### For Louisiana Dental Plan (louisianadentalplan.com):

```html
<!-- Add before closing </body> tag -->
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://your-cdn.com/chatbot.css">
<script src="https://your-cdn.com/chatbot.js"></script>
<script>
  RX4MChatbot.init({
    apiUrl: 'https://your-api-domain.com',
    site: 'louisianadental',
    position: 'bottom-right'
  });
</script>
```

## API Endpoints

### Health Check
```bash
GET /
```

### Chat
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "What are your hours?",
  "session_id": "optional-session-id",
  "site": "rx4miracles"  # or "louisianadental"
}
```

### Widget Config
```bash
GET /api/config/{site}
# Returns widget configuration (colors, greeting, etc.)
```

### SMS Webhook (Coming Soon)
```bash
POST /api/sms/webhook
# Will handle incoming SMS from Twilio
```

## Configuration

Each site has its own YAML config in the `config/` directory:

- `config/rx4miracles.yaml` - RX4 Miracles settings
- `config/louisianadental.yaml` - Louisiana Dental Plan settings

You can customize:
- Site name and branding colors
- AI model and system prompts
- Business hours and contact info
- Escalation keywords
- SMS settings

## Customization

### Change Widget Colors

Edit the `primary_color` in the site's YAML config file, or override CSS variables:

```css
:root {
  --chatbot-primary-color: #your-color;
}
```

### Change Widget Position

```javascript
RX4MChatbot.init({
  position: 'bottom-left'  // or 'bottom-right'
});
```

### Customize Greeting Message

Update the `greeting` field in the YAML config file.

### Modify AI Behavior

Edit the `system_prompt` in the YAML config to change how the AI responds.

## Deployment

### Backend Deployment (recommended: Railway, Render, Fly.io)

1. Set environment variables:
   - `OPENAI_API_KEY`
   - `CORS_ORIGINS` (production domains)

2. Deploy the `backend/` directory

3. Note the API URL

### Widget Deployment (recommended: CDN like Cloudflare, Vercel, Netlify)

1. Upload `chatbot.js` and `chatbot.css` to your CDN

2. Update integration code with CDN URLs

3. Update `apiUrl` in init() to your backend URL

## Adding SMS Support

1. Sign up for Twilio account

2. Update `.env`:
   ```
   TWILIO_ACCOUNT_SID=your-sid
   TWILIO_AUTH_TOKEN=your-token
   TWILIO_PHONE_NUMBER=your-number
   ```

3. Set `sms.enabled: true` in config YAML

4. Configure Twilio webhook to point to `/api/sms/webhook`

5. Implement SMS handler in `backend/main.py` (TODO)

## Development

### Testing the API

```bash
# Health check
curl http://localhost:8000/

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "site": "rx4miracles"
  }'

# Get widget config
curl http://localhost:8000/api/config/rx4miracles
```

### Widget Development

1. Edit `widget/chatbot.js` and `widget/chatbot.css`
2. Refresh `widget/chatbot.html` to see changes
3. Use browser dev tools to debug

## Handoff Checklist for Lead Dev

- [ ] Host `chatbot.js` and `chatbot.css` on CDN
- [ ] Deploy backend API
- [ ] Update CORS_ORIGINS with production domains
- [ ] Add widget integration code to both websites
- [ ] Test on staging before production
- [ ] Update contact info in YAML configs
- [ ] Add actual logo URLs
- [ ] Set up SSL/HTTPS for API

## Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional:
- `TWILIO_ACCOUNT_SID` - For SMS support
- `TWILIO_AUTH_TOKEN` - For SMS support
- `TWILIO_PHONE_NUMBER` - For SMS support
- `CORS_ORIGINS` - Comma-separated allowed domains
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- OpenAI API
- Twilio (for SMS)

**Frontend:**
- Vanilla JavaScript (no framework dependencies)
- CSS3
- HTML5

## Support

For questions or issues, contact the Agent Eva team.

## License

Proprietary - Agent Eva
