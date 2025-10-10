"""
Setup script for OpenAI Assistants API with Database Integration
Creates assistants and saves them to the database
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from models import Company, init_db, SessionLocal

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_assistant_for_company(company: Company) -> str:
    """
    Create an OpenAI assistant for a company using database config
    Returns: assistant_id
    """
    print(f"\n{'='*60}")
    print(f"Creating assistant for: {company.name}")
    print(f"{'='*60}")

    # Combine system prompt with knowledge base
    full_instructions = f"""{company.system_prompt}

KNOWLEDGE BASE:
{company.knowledge_base}

Use the knowledge base above to answer questions accurately. Provide responses in a natural, conversational tone without excessive markdown formatting (avoid bullet points and bold text unless specifically needed for clarity)."""

    # Create assistant
    print("Creating assistant with embedded knowledge...")
    assistant = client.beta.assistants.create(
        name=f"{company.name} Support Assistant",
        instructions=full_instructions,
        model=company.model
    )
    print(f"✓ Assistant created: {assistant.id}")

    return assistant.id


def update_assistant(company: Company) -> str:
    """
    Update an existing assistant with new content from database
    Useful when knowledge base is updated
    """
    if not company.assistant_id:
        raise ValueError(f"Company {company.site_id} has no assistant_id")

    print(f"\n{'='*60}")
    print(f"Updating assistant for: {company.name}")
    print(f"{'='*60}")

    # Combine system prompt with knowledge base
    full_instructions = f"""{company.system_prompt}

KNOWLEDGE BASE:
{company.knowledge_base}

Use the knowledge base above to answer questions accurately. Provide responses in a natural, conversational tone without excessive markdown formatting (avoid bullet points and bold text unless specifically needed for clarity)."""

    # Update assistant
    print(f"Updating assistant {company.assistant_id}...")
    assistant = client.beta.assistants.update(
        assistant_id=company.assistant_id,
        instructions=full_instructions,
        model=company.model
    )
    print(f"✓ Assistant updated: {assistant.id}")

    return assistant.id


def setup_all_assistants():
    """
    Setup assistants for all companies in database that don't have one
    """
    print("\n" + "="*60)
    print("OpenAI Assistants Setup (Database-Driven)")
    print("="*60)

    # Initialize database
    init_db()
    db = SessionLocal()

    try:
        # Get all active companies
        companies = db.query(Company).filter(Company.active == True).all()

        if not companies:
            print("\n⚠️  No companies found in database!")
            print("Run 'python seed_database.py' first to add companies.")
            return

        created_count = 0
        skipped_count = 0

        for company in companies:
            if company.assistant_id:
                print(f"\n✓ {company.name} already has assistant: {company.assistant_id}")
                skipped_count += 1
                continue

            # Create new assistant
            assistant_id = create_assistant_for_company(company)

            # Save assistant_id to database
            company.assistant_id = assistant_id
            db.commit()
            created_count += 1

        # Print summary
        print("\n" + "="*60)
        print("Setup Complete!")
        print("="*60)
        print(f"\nCreated: {created_count} assistants")
        print(f"Skipped: {skipped_count} (already configured)")
        print(f"\nAll assistant IDs saved to database.")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def update_all_assistants():
    """
    Update all existing assistants with latest content from database
    """
    print("\n" + "="*60)
    print("Updating All Assistants")
    print("="*60)

    db = SessionLocal()

    try:
        companies = db.query(Company).filter(
            Company.active == True,
            Company.assistant_id.isnot(None)
        ).all()

        for company in companies:
            update_assistant(company)
            print(f"✓ Updated {company.name}")

        print(f"\n✓ Updated {len(companies)} assistants")

    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        update_all_assistants()
    else:
        setup_all_assistants()
