"""
Database models for multi-tenant chatbot system
Uses SQLAlchemy with SQLite/PostgreSQL support
"""

from sqlalchemy import create_engine, Column, String, Integer, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class Company(Base):
    """
    Company/Tenant configuration
    Each company has their own chatbot with custom branding and knowledge
    """
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(String(50), unique=True, nullable=False, index=True)  # e.g., 'rx4miracles'
    name = Column(String(200), nullable=False)  # e.g., 'Rx4Miracles'
    domain = Column(String(200))  # e.g., 'rx4miracles.org'
    description = Column(Text)

    # Branding
    primary_color = Column(String(20))  # e.g., '#0066cc'
    greeting = Column(Text)  # Welcome message

    # AI Configuration
    assistant_id = Column(String(100))  # OpenAI Assistant ID
    model = Column(String(50), default='gpt-4o-mini')
    temperature = Column(String(10), default='0.4')
    max_tokens = Column(Integer, default=500)
    system_prompt = Column(Text)

    # Business Info (stored as JSON for flexibility)
    contact_info = Column(JSON)  # phone, email, hours, address, etc.

    # Knowledge Base
    knowledge_base = Column(Text)  # Markdown content
    faqs = Column(JSON)  # List of FAQ objects

    # Features
    sms_enabled = Column(Boolean, default=False)
    sms_phone_number = Column(String(20))

    # Metadata
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'site_id': self.site_id,
            'name': self.name,
            'domain': self.domain,
            'description': self.description,
            'branding': {
                'primary_color': self.primary_color,
                'greeting': self.greeting
            },
            'ai': {
                'assistant_id': self.assistant_id,
                'model': self.model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'system_prompt': self.system_prompt
            },
            'contact_info': self.contact_info,
            'knowledge_base': self.knowledge_base,
            'faqs': self.faqs,
            'sms': {
                'enabled': self.sms_enabled,
                'phone_number': self.sms_phone_number
            },
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ChatSession(Base):
    """
    Optional: Track chat sessions for analytics
    """
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    site_id = Column(String(50), nullable=False, index=True)
    thread_id = Column(String(100))  # OpenAI thread ID
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)


# Database connection
def get_database_url():
    """Get database URL from environment or use SQLite as fallback"""
    # Heroku sets DATABASE_URL automatically for Postgres
    database_url = os.getenv('DATABASE_URL')

    # Heroku Postgres URLs start with 'postgres://' but SQLAlchemy needs 'postgresql://'
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Fallback to SQLite for local development
    if not database_url:
        from pathlib import Path
        db_path = Path(__file__).parent / 'chatbot.db'
        database_url = f'sqlite:///{db_path}'

    return database_url


# Create engine and session
engine = create_engine(get_database_url(), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database initialized: {get_database_url()}")


def get_db():
    """Get database session (for dependency injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
