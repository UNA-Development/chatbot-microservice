# Heroku Deployment Guide

## Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository initialized

## Step 1: Install Heroku CLI
```bash
brew install heroku/brew/heroku
```

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
heroku create your-chatbot-api
```

This creates your app at: `https://your-chatbot-api.herokuapp.com`

## Step 4: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:essential-0
```

This automatically sets the DATABASE_URL environment variable.

## Step 5: Set Environment Variables
```bash
heroku config:set OPENAI_API_KEY=sk-your-actual-openai-key
```

## Step 6: Deploy to Heroku
```bash
git push heroku main
```

If your branch is named differently:
```bash
git push heroku your-branch:main
```

## Step 7: Initialize Database
Run the seed script to populate your database:
```bash
heroku run python backend/seed_database.py
```

## Step 8: Create OpenAI Assistants
```bash
heroku run python backend/setup_assistants.py
```

This creates assistants for all companies in the database and updates their assistant_id fields.

## Step 9: Verify Deployment
Check if the app is running:
```bash
heroku open
```

You should see:
```json
{
  "status": "online",
  "service": "Chatbot Microservice API",
  "version": "3.0.0",
  "rag_provider": "OpenAI Assistants API",
  "active_companies": 2
}
```

## Step 10: View Logs
Monitor your application:
```bash
heroku logs --tail
```

## Adding New Companies (No Redeployment)

After initial deployment, add new companies without redeploying:

### Option 1: Via API
Use the admin endpoints at `https://your-app.herokuapp.com/docs`

### Option 2: Via Script
```bash
heroku run python backend/quick_add_company.py
```

### Option 3: Direct Database
```bash
heroku run python
```
Then use the Python shell to add companies using the models.

## Updating Knowledge Bases (No Redeployment)

Update company knowledge via API:
```bash
curl -X PATCH https://your-app.herokuapp.com/admin/companies/{site_id}/knowledge \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base": "Updated FAQs and information..."}'
```

Then update the assistant:
```bash
heroku run python backend/setup_assistants.py --update
```

## Troubleshooting

### Build fails
Check `requirements.txt` is in the root or use Procfile to specify path.

### Database connection errors
Verify PostgreSQL addon is installed:
```bash
heroku addons
```

### OpenAI API errors
Check API key is set:
```bash
heroku config:get OPENAI_API_KEY
```

### Widget files not loading
Verify static files are being served by checking:
```
https://your-app.herokuapp.com/widget/chatbot.js
```

## Useful Commands

View app info:
```bash
heroku info
```

Restart app:
```bash
heroku restart
```

Check dyno status:
```bash
heroku ps
```

Access database:
```bash
heroku pg:psql
```

View environment variables:
```bash
heroku config
```

## Production Checklist

Before going live:
- [ ] PostgreSQL addon installed
- [ ] OPENAI_API_KEY configured
- [ ] Database seeded with companies
- [ ] Assistants created for all companies
- [ ] Widget files accessible at /widget/
- [ ] API responding at root endpoint
- [ ] Test chat with both companies
- [ ] Logs show no errors
