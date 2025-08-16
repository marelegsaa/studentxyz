"""
Database Migration Script
Run this script to add new columns to existing database
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add new columns to existing database"""
    
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("Database not found at", db_path)
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(user)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        print("Existing columns:", existing_columns)

        new_columns = [
            ('bio', 'VARCHAR(500)'),
            ('telefon', 'VARCHAR(20)'),
            ('data_nasterii', 'VARCHAR(20)'),
            ('profile_picture', 'VARCHAR(200)'),
            ('pending_email', 'VARCHAR(100)'),
            ('semestru_curent', 'VARCHAR(10) DEFAULT "1"')
        ]

        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    alter_query = f"ALTER TABLE user ADD COLUMN {column_name} {column_type}"
                    cursor.execute(alter_query)
                    print(f"✅ Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"❌ Could not add column {column_name}: {e}")
            else:
                print(f"ℹ️ Column {column_name} already exists")

        if 'semestru_curent' not in existing_columns:
            try:
                cursor.execute("UPDATE user SET semestru_curent = '1' WHERE semestru_curent IS NULL")
                print("✅ Set default values for semestru_curent")
            except sqlite3.OperationalError as e:
                print(f"❌ Could not set default values: {e}")
        
        conn.commit()

        cursor.execute("PRAGMA table_info(user)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print("\nFinal columns:", final_columns)

        cursor.execute("SELECT id, nume, an, semestru_curent FROM user LIMIT 3")
        sample_data = cursor.fetchall()
        if sample_data:
            print("\nSample data verification:")
            for row in sample_data:
                print(f"  User {row[0]}: {row[1]}, An {row[2]}, Semestru {row[3]}")
        
        conn.close()
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def backup_database():
    """Create a backup of the database before migration"""
    
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("No database to backup")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f'instance/database_backup_{timestamp}.db'
    
    try:
        with open(db_path, 'rb') as f:
            data = f.read()

        with open(backup_path, 'wb') as f:
            f.write(data)
        
        print(f"✅ Backup created: {backup_path}")
        return backup_path
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def verify_migration():
    """Verify that all expected columns exist"""
    
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("Database not found")
        return False
    
    expected_columns = [
        'id', 'nume', 'prenume', 'facultate', 'specializare', 'an', 
        'email', 'password', 'confirmed', 'bio', 'telefon', 
        'data_nasterii', 'profile_picture', 'pending_email', 'semestru_curent'
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(user)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        missing_columns = set(expected_columns) - set(existing_columns)
        extra_columns = set(existing_columns) - set(expected_columns)
        
        print("\n" + "="*50)
        print("MIGRATION VERIFICATION")
        print("="*50)
        
        if not missing_columns and not extra_columns:
            print("✅ Perfect! All expected columns are present.")
        else:
            if missing_columns:
                print(f"❌ Missing columns: {missing_columns}")
            if extra_columns:
                print(f"ℹ️ Extra columns: {extra_columns}")
        
        print(f"\nTotal columns: {len(existing_columns)}")
        print(f"Expected columns: {len(expected_columns)}")
        
        conn.close()
        return len(missing_columns) == 0
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE MIGRATION SCRIPT")
    print("=" * 50)

    print("\n1. Creating backup...")
    backup_path = backup_database()
    
    if backup_path:
        print("\n2. Starting migration...")
        success = migrate_database()
        
        if success:
            print("\n3. Verifying migration...")
            verify_migration()
            print("\n✅ Migration completed! You can now run your application.")
            print("\n⚠️ Don't forget to:")
            print("   - Update your models.py with the semestru_curent field")
            print("   - Remove the migrate_database() call from main.py")
        else:
            print(f"\n❌ Migration failed. Restore from backup: {backup_path}")
    else:
        response = input("\n⚠️ No backup created. Continue anyway? (y/n): ")
        if response.lower() == 'y':
            success = migrate_database()
            if success:
                verify_migration()
        else:
            print("Migration cancelled.")