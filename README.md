# Chatbot Microservice

AI-powered multi-tenant chat support platform that can host **unlimited companies** from a single deployment.

## 🎯 Key Features

- 🚀 **No Redeployment Needed** - Add companies and update content via API
- 🏢 **Multi-Tenant** - One server, unlimited chatbots
- 🤖 **OpenAI GPT-4 powered** conversations
- 💾 **Database-Driven** - PostgreSQL/SQLite for configs
- 🎨 **Per-Company Branding** - Custom colors, greetings, knowledge
- 📱 **Mobile Responsive** widget
- 🔌 **Admin API** - Full CRUD for companies
- ⚡ **Production Ready** - Heroku, Railway, or any platform

## 📋 What's New (v3.0 - Multi-Tenant)

**Before:** YAML files, hardcoded companies, redeploy for every change
**Now:** Database-driven, add companies via API, zero downtime updates

## Project Structure

```
chatbot-microservice/
├── backend/
│   ├── main.py              # FastAPI server (database-driven)
│   ├── models.py            # Database models (SQLAlchemy)
│   ├── admin_api.py         # Admin CRUD endpoints
│   ├── seed_database.py     # Import YAML → Database
│   ├── setup_assistants.py  # Create/update OpenAI assistants
│   ├── quick_add_company.py # Interactive company creator
│   └── requirements.txt     # Python dependencies
├── widget/
│   ├── chatbot.html         # Demo page
│   ├── chatbot.js           # Widget JavaScript
│   └── chatbot.css          # Widget styles
├── config/                  # Legacy YAML (for migration only)
│   ├── rx4miracles.yaml
│   └── louisianadental.yaml
├── content/                 # Legacy markdown (for migration only)
├── Procfile                 # Heroku deployment config
├── DEPLOYMENT.md            # Full deployment guide
├── .env.example             # Environment variables template
└── README.md
```

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
cd ..
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Initialize Database

```bash
cd backend
python seed_database.py  # Imports existing companies to database
python setup_assistants.py  # Creates OpenAI assistants
```

### 4. Run Server

```bash
python main.py
# or
uvicorn main:app --reload
```

Server: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### 5. Test the Widget

Open `widget/chatbot.html` in your browser.

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

## 📦 Deployment to Heroku

Your lead dev can deploy this with these simple steps:

```bash
# 1. Create Heroku app
heroku create my-chatbot-api

# 2. Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 3. Set environment
heroku config:set OPENAI_API_KEY=sk-your-key

# 4. Deploy
git push heroku main

# 5. Initialize database (one time only)
heroku run bash
cd backend
python seed_database.py
python setup_assistants.py
exit
```

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.**

## 🎯 Adding New Companies (After Deployment)

### Method 1: Admin API (No Redeployment!)

```bash
curl -X POST https://your-api.herokuapp.com/api/admin/companies \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": "newcompany",
    "name": "New Company Inc",
    "primary_color": "#ff6600",
    "greeting": "Welcome!",
    "system_prompt": "You are a helpful assistant...",
    "knowledge_base": "## About\nNew company information..."
  }'
```

Then create the assistant:
```bash
heroku run python backend/setup_assistants.py
```

### Method 2: Interactive Script

```bash
heroku run bash
cd backend
python quick_add_company.py
# Follow the prompts
```

## 📝 Updating Knowledge Base (No Redeployment!)

```bash
curl -X PATCH https://your-api.herokuapp.com/api/admin/companies/rx4miracles/knowledge \
  -d '{"knowledge_base": "Updated content..."}'

# Then sync the assistant
heroku run python backend/setup_assistants.py --update
```

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

## 🔌 Admin API Endpoints

All available at `/api/admin/*`:

- `GET /api/admin/companies` - List all companies
- `GET /api/admin/companies/{site_id}` - Get specific company
- `POST /api/admin/companies` - Create new company
- `PATCH /api/admin/companies/{site_id}` - Update company
- `DELETE /api/admin/companies/{site_id}` - Deactivate company
- `POST /api/admin/companies/{site_id}/activate` - Reactivate company
- `PATCH /api/admin/companies/{site_id}/knowledge` - Update knowledge only

**Interactive API docs:** `https://your-api.herokuapp.com/docs`

## ✅ Handoff Checklist for Lead Dev

**Pre-Deployment:**
- [ ] Review and test locally
- [ ] Add `OPENAI_API_KEY` to `.env`
- [ ] Run `seed_database.py` and `setup_assistants.py`

**Heroku Deployment:**
- [ ] Create Heroku app
- [ ] Add PostgreSQL addon
- [ ] Set `OPENAI_API_KEY` config var
- [ ] Deploy via `git push heroku main`
- [ ] Run database seed and setup scripts (one time)

**Widget Integration:**
- [ ] Host `chatbot.js` and `chatbot.css` on CDN or Vercel
- [ ] Add widget code to rx4miracles.org
- [ ] Add widget code to louisianadentalplan.com
- [ ] Test on staging environments first
- [ ] Verify chatbot loads and responds

**Post-Launch:**
- [ ] Monitor Heroku logs for errors
- [ ] Test adding a new company via API
- [ ] Test updating knowledge base via API
- [ ] Document any custom changes

## 🛠️ Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API)
- SQLAlchemy (ORM)
- PostgreSQL (Heroku) / SQLite (local)
- OpenAI Assistants API
- Twilio (SMS - optional)

**Frontend:**
- Vanilla JavaScript (no dependencies)
- CSS3
- HTML5

## 📚 Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API docs (ReDoc)

## 🆘 Support

For questions or issues, contact the development team.

## 📄 License

Proprietary - Agent Eva
