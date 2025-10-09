"""
Setup script for OpenAI Assistants API
Creates assistants and uploads knowledge base files
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_site_config(site_name: str) -> dict:
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / 'config' / f'{site_name}.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_assistant(site_name: str) -> str:
    """
    Create an assistant for a site with knowledge embedded in instructions
    Returns: assistant_id
    """
    print(f"\n{'='*60}")
    print(f"Setting up assistant for: {site_name}")
    print(f"{'='*60}")

    # Load site config
    config = load_site_config(site_name)

    # Load knowledge base and add to system prompt
    knowledge_file_path = Path(__file__).parent.parent / 'content' / site_name / 'knowledge.md'
    print(f"Loading knowledge base: {knowledge_file_path.name}")

    with open(knowledge_file_path, 'r') as f:
        knowledge_content = f.read()

    # Combine system prompt with knowledge
    full_instructions = f"""{config['ai']['system_prompt']}

KNOWLEDGE BASE:
{knowledge_content}

Use the knowledge base above to answer questions accurately. Provide responses in a natural, conversational tone without excessive markdown formatting (avoid bullet points and bold text unless specifically needed for clarity)."""

    # Create assistant without file_search (faster responses)
    print("Creating assistant with embedded knowledge...")
    assistant = client.beta.assistants.create(
        name=f"{config['site']['name']} Support Assistant",
        instructions=full_instructions,
        model=config['ai']['model']
    )
    print(f"✓ Assistant created: {assistant.id}")

    return assistant.id

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("OpenAI Assistants API Setup")
    print("="*60)

    assistants = {}

    # Setup both sites
    for site in ['rx4miracles', 'louisianadental']:
        assistant_id = setup_assistant(site)
        assistants[site] = assistant_id

    # Print summary
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nAdd these to your .env file:")
    print()
    print(f"RX4M_ASSISTANT_ID={assistants['rx4miracles']}")
    print(f"LOUISIANA_ASSISTANT_ID={assistants['louisianadental']}")
    print()
    print("="*60)

    return assistants

if __name__ == "__main__":
    main()
