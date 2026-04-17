import sqlite3
import uuid

def get_db():
    conn = sqlite3.connect('profiles.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            gender TEXT,
            gender_probability REAL,
            sample_size INTEGER,
            age INTEGER,
            age_group TEXT,
            country_id TEXT,
            country_probability REAL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_profile(profile_data):
    conn = get_db()
    conn.execute('''
        INSERT OR REPLACE INTO profiles 
        (id, name, gender, gender_probability, sample_size, age, age_group, country_id, country_probability, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        profile_data['id'],
        profile_data['name'],
        profile_data['gender'],
        profile_data['gender_probability'],
        profile_data['sample_size'],
        profile_data['age'],
        profile_data['age_group'],
        profile_data['country_id'],
        profile_data['country_probability'],
        profile_data['created_at']
    ))
    conn.commit()
    conn.close()

def get_profile_by_name(name):
    conn = get_db()
    profile = conn.execute('SELECT * FROM profiles WHERE name = ?', (name.lower(),)).fetchone()
    conn.close()
    return profile

def get_profile_by_id(profile_id):
    conn = get_db()
    profile = conn.execute('SELECT * FROM profiles WHERE id = ?', (profile_id,)).fetchone()
    conn.close()
    return profile

def get_all_profiles(filters=None):
    conn = get_db()
    query = 'SELECT id, name, gender, age, age_group, country_id FROM profiles'
    params = []
    
    if filters:
        conditions = []
        if filters.get('gender'):
            conditions.append('gender = ?')
            params.append(filters['gender'].lower())
        if filters.get('country_id'):
            conditions.append('country_id = ?')
            params.append(filters['country_id'].upper())
        if filters.get('age_group'):
            conditions.append('age_group = ?')
            params.append(filters['age_group'].lower())
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
    
    profiles = conn.execute(query, params).fetchall()
    conn.close()
    return profiles

def delete_profile(profile_id):
    conn = get_db()
    conn.execute('DELETE FROM profiles WHERE id = ?', (profile_id,))
    conn.commit()
    conn.close()