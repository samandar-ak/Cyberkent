import sqlite3

DATABASE = 'documents.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'admin' 
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            size TEXT NOT NULL,
            extension TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            description TEXT,
            file_path TEXT NOT NULL,
            user_id INTEGER NOT NULL, 
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, role) 
        VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_password(username, new_password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET password = ?
        WHERE username = ?
    ''', (new_password, username))
    conn.commit()
    conn.close()


def get_username_by_id(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else None


def add_document(doc_info):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documents (name, size, extension, upload_date, description, file_path, user_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (doc_info['name'], doc_info['size'], doc_info['extension'], doc_info['upload_date'], doc_info['description'], doc_info['file_path'], doc_info['user_id']))
    conn.commit()
    conn.close()

def get_documents():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents')
    documents = cursor.fetchall()
    conn.close()
    return documents

def get_documents_by_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents WHERE user_id = ?', (user_id,))
    documents = cursor.fetchall()
    conn.close()
    return documents

def get_document_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def delete_document(doc_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
    conn.commit()
    conn.close()

def get_document(doc_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents WHERE name = ?', (doc_id,))
    document = cursor.fetchone()
    conn.close()
    return document

def get_document_by_name(name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE name = ?", (name,))
    document = cursor.fetchone()
    conn.close()
    return document

def delete_document_by_name(doc_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()   
    cursor.execute("DELETE FROM documents WHERE name = ?", (doc_name,))
    conn.commit()
    conn.close()



def update_document(doc_id, name, description, size, extension, upload_date, file_path):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE documents
        SET name = ?, description = ?, size = ?, extension = ?, upload_date = ?, file_path = ?
        WHERE id = ?
    ''', (name, description, size, extension, upload_date, file_path, doc_id))
    conn.commit()
    conn.close()
