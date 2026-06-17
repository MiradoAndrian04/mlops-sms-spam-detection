import sqlite3
conn = sqlite3.connect('/app/mlflow.db')
cursor = conn.cursor()

# Lister toutes les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('='*50)
print('🗄️  TABLES DANS MLFLOW.DB')
print('='*50)

if tables:
    for table in tables:
        print(f'\n📋 Table: {table[0]}')
        
        # Compter les lignes
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'   Lignes: {count}')
        
        # Afficher les colonnes
        cursor.execute(f'PRAGMA table_info({table[0]})')
        columns = cursor.fetchall()
        print(f'   Colonnes: {len(columns)}')
        for col in columns[:5]:
            print(f'      - {col[1]} ({col[2]})')
else:
    print('❌ Aucune table trouvée.')

conn.close()
