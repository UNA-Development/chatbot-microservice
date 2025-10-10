"""
Seed database with existing YAML configurations
Run this once to migrate from YAML to database
"""

import yaml
from pathlib import Path
from models import Company, init_db, SessionLocal
import os
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)


def load_yaml_config(site_id: str) -> dict:
    """Load YAML configuration"""
    config_path = Path(__file__).parent.parent / 'config' / f'{site_id}.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_knowledge_base(site_id: str) -> str:
    """Load knowledge base markdown file"""
    knowledge_path = Path(__file__).parent.parent / 'content' / site_id / 'knowledge.md'
    if knowledge_path.exists():
        with open(knowledge_path, 'r') as f:
            return f.read()
    return ""


def seed_company(db, site_id: str, assistant_id: str = None):
    """Seed a single company from YAML config"""

    # Check if company already exists
    existing = db.query(Company).filter(Company.site_id == site_id).first()
    if existing:
        print(f"⚠ Company '{site_id}' already exists, skipping...")
        return existing

    print(f"\n📦 Seeding company: {site_id}")

    # Load config and knowledge
    config = load_yaml_config(site_id)
    knowledge = load_knowledge_base(site_id)

    # Create company record
    company = Company(
        site_id=site_id,
        name=config['site']['name'],
        domain=config['site'].get('domain', ''),
        description=config['site'].get('description', ''),

        # Branding
        primary_color=config['branding'].get('primary_color', '#0066cc'),
        greeting=config['branding'].get('greeting', 'Hello! How can I help you today?'),

        # AI config
        assistant_id=assistant_id,
        model=config['ai'].get('model', 'gpt-4o-mini'),
        temperature=str(config['ai'].get('temperature', 0.4)),
        max_tokens=config['ai'].get('max_tokens', 500),
        system_prompt=config['ai'].get('system_prompt', ''),

        # Contact info
        contact_info=config.get('business', {}).get('contact', {}),

        # Knowledge and FAQs
        knowledge_base=knowledge,
        faqs=config.get('faqs', []),

        # SMS config
        sms_enabled=config.get('sms', {}).get('enabled', False),
        sms_phone_number=config.get('sms', {}).get('phone_number', ''),

        active=True
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    print(f"✓ Created company: {company.name} (ID: {company.id})")
    return company


def main():
    """Main seeding function"""
    print("="*60)
    print("Database Seeding Script")
    print("="*60)

    # Initialize database
    print("\n🗄️  Initializing database...")
    init_db()

    # Create session
    db = SessionLocal()

    try:
        # Seed companies
        companies = {
            'rx4miracles': os.getenv('RX4M_ASSISTANT_ID'),
            'louisianadental': os.getenv('LOUISIANA_ASSISTANT_ID')
        }

        for site_id, assistant_id in companies.items():
            seed_company(db, site_id, assistant_id)

        print("\n" + "="*60)
        print("✅ Database seeding complete!")
        print("="*60)

        # Show summary
        total_companies = db.query(Company).count()
        print(f"\nTotal companies in database: {total_companies}")

        for company in db.query(Company).all():
            print(f"  • {company.name} ({company.site_id}) - Assistant: {company.assistant_id or 'Not set'}")

    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
