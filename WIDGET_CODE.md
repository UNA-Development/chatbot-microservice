# Pre-Deployment Testing Checklist

## 🎯 Complete Testing Guide Before Handoff to Lead Developer

Run through this checklist to ensure everything works perfectly.

---

## ✅ Phase 1: Database & Setup Tests

### 1.1 Database Initialization
```bash
cd backend
venv/bin/python seed_database.py
```

**Expected:**
- ✅ "Database seeding complete!"
- ✅ Shows 2 companies created (rx4miracles, louisianadental)
- ✅ No errors

### 1.2 Assistant Setup
```bash
venv/bin/python setup_assistants.py
```

**Expected:**
- ✅ "Setup Complete!"
- ✅ Shows assistant IDs for both companies
- ✅ No errors

### 1.3 Database Verification
```bash
venv/bin/python -c "from models import *; db = SessionLocal(); print(f'Companies: {db.query(Company).count()}'); [print(f'  - {c.name} ({c.site_id})') for c in db.query(Company).all()]"
```

**Expected:**
- ✅ Shows company count
- ✅ Lists all companies with names and site_ids

---

## ✅ Phase 2: API Endpoint Tests

### 2.1 Start Server
```bash
venv/bin/python main.py
```

**Expected:**
- ✅ "Database connected: X companies loaded"
- ✅ "Uvicorn running on http://0.0.0.0:8000"
- ✅ No errors

**Keep this running for all tests below!**

---

### 2.2 Health Check
```bash
curl http://localhost:8000/
```

**Expected:**
```json
{
  "status": "online",
  "service": "Chatbot Microservice API",
  "version": "3.0.0",
  "rag_provider": "OpenAI Assistants API",
  "active_companies": 2
}
```

---

### 2.3 List All Companies
```bash
curl http://localhost:8000/api/admin/companies | python3 -m json.tool
```

**Expected:**
- ✅ Returns array of company objects
- ✅ Each has: id, site_id, name, branding, ai, contact_info, etc.
- ✅ Both companies present

---

### 2.4 Get Specific Company
```bash
curl http://localhost:8000/api/admin/companies/rx4miracles | python3 -m json.tool
```

**Expected:**
- ✅ Returns single company object
- ✅ Has assistant_id
- ✅ Has knowledge_base content
- ✅ All fields populated

---

### 2.5 Get Widget Config
```bash
curl http://localhost:8000/api/config/rx4miracles | python3 -m json.tool
```

**Expected:**
```json
{
  "site_name": "Rx4Miracles",
  "primary_color": "#0066cc",
  "greeting_message": "Hey! I'm here to help..."
}
```

---

## ✅ Phase 3: Chat Functionality Tests

### 3.1 Test Chat - Rx4Miracles
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your hours?", "site": "rx4miracles"}'
```

**Expected:**
- ✅ Returns JSON with "response", "session_id", "timestamp"
- ✅ Response mentions 24/7 availability
- ✅ No errors

### 3.2 Test Chat - Louisiana Dental
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How much does a family plan cost?", "site": "louisianadental"}'
```

**Expected:**
- ✅ Returns JSON with response
- ✅ Response mentions $12/month for family
- ✅ No errors

### 3.3 Test Chat - Different Questions
```bash
# Rx4Miracles - Pharmacy question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What pharmacies accept this card?", "site": "rx4miracles"}'

# Louisiana Dental - Savings question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How much can I save?", "site": "louisianadental"}'
```

**Expected:**
- ✅ Both return relevant, accurate responses
- ✅ Responses match knowledge base content
- ✅ No hallucinations or wrong info

---

## ✅ Phase 4: Admin Operations Tests

### 4.1 Create New Company
```bash
curl -X POST http://localhost:8000/api/admin/companies \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": "testco",
    "name": "Test Company",
    "domain": "test.com",
    "description": "A test company",
    "primary_color": "#ff0000",
    "greeting": "Hello from Test Co!",
    "system_prompt": "You are a helpful assistant for Test Company.",
    "knowledge_base": "## About\nTest Company provides testing services.\n\n## Hours\nMonday-Friday 9-5",
    "contact_info": {"phone": "555-1234"}
  }'
```

**Expected:**
- ✅ Returns 200/201 status
- ✅ Returns company object with id=3
- ✅ assistant_id is null (not created yet)

### 4.2 Create Assistant for New Company
```bash
venv/bin/python setup_assistants.py
```

**Expected:**
- ✅ "Created: 1 assistants"
- ✅ "Skipped: 2 (already configured)"
- ✅ Shows assistant ID for testco

### 4.3 Test Chat with New Company
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your hours?", "site": "testco"}'
```

**Expected:**
- ✅ Returns response about Monday-Friday 9-5
- ✅ Works immediately after assistant creation

### 4.4 Update Company Knowledge
```bash
curl -X PATCH http://localhost:8000/api/admin/companies/testco/knowledge \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base": "## About\nUPDATED content.\n\n## Hours\nNow 24/7!"}'
```

**Expected:**
- ✅ Returns success message
- ✅ Shows updated_at timestamp

### 4.5 Update Assistant with New Knowledge
```bash
venv/bin/python setup_assistants.py --update
```

**Expected:**
- ✅ "Updated 3 assistants" (or however many you have)
- ✅ No errors

### 4.6 Verify Updated Knowledge
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your hours now?", "site": "testco"}'
```

**Expected:**
- ✅ Response mentions 24/7 (the updated hours)

### 4.7 Update Company Branding
```bash
curl -X PATCH http://localhost:8000/api/admin/companies/testco \
  -H "Content-Type: application/json" \
  -d '{"primary_color": "#00ff00", "greeting": "NEW GREETING!"}'
```

**Expected:**
- ✅ Returns updated company object
- ✅ Shows new color and greeting

### 4.8 Deactivate Company
```bash
curl -X DELETE http://localhost:8000/api/admin/companies/testco
```

**Expected:**
- ✅ Returns success message
- ✅ Company deactivated (not deleted)

### 4.9 Try to Chat with Deactivated Company
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "site": "testco"}'
```

**Expected:**
- ✅ Returns 404 error
- ✅ Message: "Company 'testco' not found or inactive"

### 4.10 Reactivate Company
```bash
curl -X POST http://localhost:8000/api/admin/companies/testco/activate
```

**Expected:**
- ✅ Returns success message
- ✅ Company active again

### 4.11 Chat Works Again
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "site": "testco"}'
```

**Expected:**
- ✅ Returns response successfully
- ✅ Company works again

---

## ✅ Phase 5: Error Handling Tests

### 5.1 Invalid Site ID
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "site": "nonexistent"}'
```

**Expected:**
- ✅ Returns 404 error
- ✅ Clear error message

### 5.2 Missing Required Fields
```bash
curl -X POST http://localhost:8000/api/admin/companies \
  -H "Content-Type: application/json" \
  -d '{"site_id": "incomplete"}'
```

**Expected:**
- ✅ Returns 422 validation error
- ✅ Shows which fields are required

### 5.3 Duplicate Site ID
```bash
curl -X POST http://localhost:8000/api/admin/companies \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": "rx4miracles",
    "name": "Duplicate",
    "system_prompt": "Test",
    "knowledge_base": "Test"
  }'
```

**Expected:**
- ✅ Returns 400 error
- ✅ Message about duplicate site_id

### 5.4 Empty Chat Message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "", "site": "rx4miracles"}'
```

**Expected:**
- ✅ Returns validation error
- ✅ Message about min length

---

## ✅ Phase 6: Widget Tests

### 6.1 Open Widget Demo
```bash
open widget/chatbot.html
# Or manually navigate to the file in browser
```

**Expected:**
- ✅ Chat button appears in bottom right
- ✅ Button has correct styling
- ✅ No console errors

### 6.2 Open Chat Window
**Action:** Click the chat button

**Expected:**
- ✅ Chat window opens
- ✅ Typing indicator appears
- ✅ Greeting message appears after 1.5 seconds
- ✅ Input field is focused

### 6.3 Send Message
**Action:** Type "What are your hours?" and hit Enter

**Expected:**
- ✅ Message appears in chat
- ✅ Typing indicator shows
- ✅ Bot response appears
- ✅ Response is relevant
- ✅ No errors in console

### 6.4 Test Different Company
**Action:** Edit `widget/chatbot.html` and change:
```javascript
site: 'louisianadental'
```

**Expected:**
- ✅ Different greeting message
- ✅ Different color (green instead of blue)
- ✅ Responses specific to Louisiana Dental

---

## ✅ Phase 7: Interactive API Docs

### 7.1 Access Swagger UI
```bash
open http://localhost:8000/docs
```

**Expected:**
- ✅ Page loads successfully
- ✅ Shows all endpoints
- ✅ Grouped into "admin" and "default"

### 7.2 Test Endpoint via Swagger
**Action:**
1. Find "GET /api/admin/companies"
2. Click "Try it out"
3. Click "Execute"

**Expected:**
- ✅ Shows request URL
- ✅ Shows response (list of companies)
- ✅ Response code 200

### 7.3 Test POST via Swagger
**Action:**
1. Find "POST /api/admin/companies"
2. Click "Try it out"
3. Fill in example company data
4. Click "Execute"

**Expected:**
- ✅ Company created
- ✅ Returns company object
- ✅ Shows in company list

---

## ✅ Phase 8: Performance Tests

### 8.1 Response Time Test
```bash
time curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "site": "rx4miracles"}'
```

**Expected:**
- ✅ Response in < 10 seconds
- ✅ Usually 2-6 seconds depending on OpenAI

### 8.2 Multiple Requests
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Test $i\", \"site\": \"rx4miracles\"}" &
done
wait
```

**Expected:**
- ✅ All 5 requests complete successfully
- ✅ No server crashes
- ✅ No database locks

---

## ✅ Phase 9: Documentation Verification

### 9.1 README Accuracy
**Action:** Read through README.md

**Check:**
- ✅ Installation steps work
- ✅ Commands are correct
- ✅ Examples match actual API responses
- ✅ No references to old "RX4M" naming

### 9.2 DEPLOYMENT.md Accuracy
**Action:** Read through DEPLOYMENT.md

**Check:**
- ✅ Heroku setup steps are clear
- ✅ Environment variables documented
- ✅ Database setup explained
- ✅ No outdated information

### 9.3 Quick Reference Accuracy
**Action:** Read QUICK_REFERENCE.md

**Check:**
- ✅ Commands work as shown
- ✅ Examples produce expected output
- ✅ URLs are correct

---

## ✅ Phase 10: Code Quality Checks

### 10.1 No Syntax Errors
```bash
cd backend
venv/bin/python -m py_compile *.py
```

**Expected:**
- ✅ No errors
- ✅ All files compile

### 10.2 Dependencies Installable
```bash
pip install -r requirements.txt
```

**Expected:**
- ✅ All packages install successfully
- ✅ No version conflicts

### 10.3 Environment Template Complete
**Action:** Compare `.env` with `.env.example`

**Check:**
- ✅ All required vars in `.env.example`
- ✅ No secrets in `.env.example`
- ✅ Clear descriptions

---

## ✅ Final Checklist Summary

Before handing off to your lead dev, verify:

- [ ] Database seeds successfully
- [ ] Assistants create successfully
- [ ] All API endpoints work
- [ ] Chat works for both companies
- [ ] Can add new company via API
- [ ] Can update knowledge via API
- [ ] Error handling works properly
- [ ] Widget loads and functions
- [ ] Documentation is accurate
- [ ] No console errors
- [ ] No server crashes
- [ ] Archive folder created (legacy files moved)
- [ ] .gitignore updated
- [ ] All tests pass

---

## 🎁 Handoff Package

When everything passes, provide your lead dev with:

1. ✅ Link to git repository
2. ✅ This testing checklist (completed)
3. ✅ DEPLOYMENT.md for Heroku setup
4. ✅ QUICK_REFERENCE.md for common tasks
5. ✅ Access to OpenAI API key (via secure method)
6. ✅ Note about which companies are already in the system

---

## 🆘 If Something Fails

**Server won't start:**
- Check `.env` has OPENAI_API_KEY
- Check database initialized: `python seed_database.py`
- Check logs for specific error

**Chat doesn't respond:**
- Verify assistant_id exists in database
- Check OpenAI API key is valid
- Check OpenAI dashboard for assistant

**Database errors:**
- Delete `backend/chatbot.db` and re-seed
- Check SQLAlchemy version in requirements.txt

**Widget doesn't load:**
- Check browser console for errors
- Verify apiUrl points to running server
- Check CORS settings in main.py

---

## 📊 Test Results Template

Copy this to share with your lead dev:

```
TESTING RESULTS - Chatbot Microservice
Date: ___________
Tested By: ___________

✅ Database & Setup: PASS / FAIL
✅ API Endpoints: PASS / FAIL
✅ Chat Functionality: PASS / FAIL
✅ Admin Operations: PASS / FAIL
✅ Error Handling: PASS / FAIL
✅ Widget: PASS / FAIL
✅ Documentation: PASS / FAIL
✅ Performance: PASS / FAIL

Notes:
_________________________________
_________________________________

Ready for Production: YES / NO
```
