"""
Quick helper script to add a new company interactively
Usage: python quick_add_company.py
"""

from models import Company, init_db, SessionLocal
from setup_assistants import create_assistant_for_company


def interactive_add_company():
    """Interactive prompt to add a new company"""
    print("\n" + "="*60)
    print("Add New Company")
    print("="*60)

    # Get basic info
    site_id = input("\nSite ID (e.g., 'mycompany'): ").strip()
    name = input("Company Name (e.g., 'My Company Inc'): ").strip()
    domain = input("Domain (e.g., 'mycompany.com'): ").strip()
    description = input("Short description: ").strip()

    # Branding
    primary_color = input("Primary color (default: #0066cc): ").strip() or "#0066cc"
    greeting = input("Greeting message: ").strip()

    # AI settings
    model = input("Model (default: gpt-4o-mini): ").strip() or "gpt-4o-mini"
    system_prompt = input("System prompt (instructions for AI): ").strip()

    # Knowledge
    print("\nKnowledge Base (type 'END' on a new line when done):")
    knowledge_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        knowledge_lines.append(line)
    knowledge_base = '\n'.join(knowledge_lines)

    # Contact info
    phone = input("\nContact phone: ").strip()
    email = input("Contact email: ").strip()
    website = input("Website: ").strip()

    contact_info = {
        "phone": phone,
        "email": email,
        "website": website
    }

    # Initialize database
    init_db()
    db = SessionLocal()

    try:
        # Check if exists
        existing = db.query(Company).filter(Company.site_id == site_id).first()
        if existing:
            print(f"\n❌ Company '{site_id}' already exists!")
            return

        # Create company
        company = Company(
            site_id=site_id,
            name=name,
            domain=domain,
            description=description,
            primary_color=primary_color,
            greeting=greeting,
            model=model,
            temperature="0.4",
            max_tokens=500,
            system_prompt=system_prompt,
            knowledge_base=knowledge_base,
            contact_info=contact_info,
            faqs=[],
            sms_enabled=False,
            active=True
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        print(f"\n✅ Company '{name}' created successfully!")

        # Offer to create assistant
        create_assistant = input("\nCreate OpenAI assistant now? (y/n): ").strip().lower()
        if create_assistant == 'y':
            assistant_id = create_assistant_for_company(company)
            company.assistant_id = assistant_id
            db.commit()
            print(f"✅ Assistant created: {assistant_id}")

        print("\n" + "="*60)
        print("Company Details:")
        print("="*60)
        print(f"Site ID: {company.site_id}")
        print(f"Name: {company.name}")
        print(f"Assistant ID: {company.assistant_id or 'Not created'}")
        print("\nWidget integration code:")
        print(f"""
<script src="YOUR_API_URL/widget/chatbot.js"></script>
<script>
  window.chatbotConfig = {{
    site: '{company.site_id}',
    apiUrl: 'YOUR_API_URL'
  }};
</script>
        """)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    interactive_add_company()
