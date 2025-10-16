"""
Simple database initialization script
Creates empty database tables - no seed data required
"""

from models import init_db, SessionLocal, Company

def main():
    print("="*60)
    print("Database Initialization")
    print("="*60)

    # Initialize database tables
    print("\n🗄️  Creating database tables...")
    init_db()

    # Check if any companies exist
    db = SessionLocal()
    try:
        company_count = db.query(Company).count()
        print(f"\n✅ Database initialized successfully!")
        print(f"📊 Current companies in database: {company_count}")

        if company_count == 0:
            print("\n💡 Database is empty. Add companies using one of these methods:")
            print("   1. Run: python quick_add_company.py")
            print("   2. Use Admin API: POST /api/admin/companies")
            print("   3. Visit API docs: https://your-app.herokuapp.com/docs")
        else:
            print("\n📋 Existing companies:")
            for company in db.query(Company).all():
                status = "✅ Active" if company.active else "❌ Inactive"
                assistant = f"Assistant: {company.assistant_id}" if company.assistant_id else "⚠️  No assistant"
                print(f"   • {company.name} ({company.site_id}) - {status} - {assistant}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        db.close()

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
