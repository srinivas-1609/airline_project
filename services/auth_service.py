import sqlite3
from database.database import get_connection
from services import data_store

class AuthService:
    @staticmethod
    def login(username, password):
        """Authenticates a user via O(1) Hash Table lookup."""
        # Using user_hash and .search()
        user = data_store.user_hash.search(username)
        if user and user['password'] == password:
            return user
        return None

    @staticmethod
    def register_passenger(name, username, password):
        """Registers a new passenger in SQLite and the Hash Table."""
        # Using user_hash and .search()
        if data_store.user_hash.search(username):
            return False, "Username already exists! Please choose another."

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)', 
                           (username, password, 'passenger', name))
            conn.commit()
            
            cursor.execute('SELECT last_insert_rowid()')
            user_id = cursor.fetchone()[0]
            conn.close()
            
            user_data = {
                'user_id': user_id, 
                'username': username, 
                'password': password, 
                'role': 'passenger', 
                'name': name
            }
            # Using user_hash and .insert()
            data_store.user_hash.insert(username, user_data)
            
            return True, "Account created successfully! You can now log in."
            
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Username already taken in database."