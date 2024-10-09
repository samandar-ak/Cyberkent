import os
from flask import Flask, render_template, abort,request, redirect, url_for, session,flash
from db import init_db,add_document,get_documents,\
            get_document_count,delete_document,get_document,\
            update_document,DATABASE,get_user,add_user,\
            get_documents_by_user,update_password,get_username_by_id,get_document_by_name,delete_document_by_name
import sqlite3
from utils import allowed_file
from datetime import datetime
import urllib.request


app = Flask(__name__)
app.secret_key = 'supersecretkey1'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


def ensure_uploads_directory_exists():
    uploads_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created directory: {uploads_dir}")

@app.errorhandler(413)
def file_too_large(error):
    flash('File size exceeds the maximum limit of 16 MB.', 'danger')
    return redirect(url_for('admin'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]  
            session['role'] = user[3]
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password!', 'danger')
    elif 'logged_in'  in session:
        return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'admin'
        if get_user(username) is None:  
            add_user(username, password, role)
            flash('User registered successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'danger')
    return render_template('register.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    
    documents = get_documents_by_user(session['user_id']) 

    if request.method == 'POST':
        if request.form.get('action') == 'add':
            file = request.files['file']
            if file and allowed_file(file.filename):
                ensure_uploads_directory_exists()
                document_name = request.form['name']
                unique_check_response = get_document_by_name(document_name)
                
                if unique_check_response:
                    flash('Document name must be unique. Please choose a different name.', 'danger')
                else:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_path)

                    upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    doc_info = {
                        'name': document_name,
                        'size': str(os.path.getsize(file_path)),
                        'extension': file.filename.split('.')[-1],
                        'upload_date': upload_date,
                        'description': request.form['description'],
                        'file_path': file_path,
                        'user_id': session['user_id'] 
                    }
                    add_document(doc_info)
                    flash('Document added successfully!', 'success')
                    documents = get_documents_by_user(session['user_id']) 

            else:
                flash('Invalid file type or no file uploaded.', 'danger')

        elif request.form.get('action') == 'delete':
            doc_name = request.form['name']  # Get document name from form
            delete_document_by_name(doc_name)  # Call a new delete function using the document name
            flash(f'Document "{doc_name}" deleted.', 'success')

    return render_template('admin.html', documents=documents)


@app.route('/document/<string:doc_name>', methods=['GET', 'POST'])
def document_detail(doc_name):

    if 'logged_in' not in session:
        return redirect(url_for('login'))

    document = get_document_by_name(doc_name)

    if document is None:
        flash('Document not found!', 'danger')
        return redirect(url_for('admin'))

    username = get_username_by_id(document[7]) if document[7] else 'Unknown'

    if session['role'] != 'admin':
        flash('You do not have permission to edit this document!', 'danger')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        if request.form.get('action') == 'edit':
            new_name = request.form['name']
            new_description = request.form['description']
            file = request.files.get('file')
            file_path = document[6]  

            existing_document = get_document_by_name(new_name)
            if existing_document and existing_document[1] != doc_name:
                flash('Document name must be unique. Please choose a different name.', 'danger')
                return redirect(url_for('document_detail', doc_name=doc_name))

            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

            update_document(document[0], new_name, new_description, document[2], document[3], document[4], file_path)
            flash('File edited successfully.', 'success')
            return redirect(url_for('admin'))

    return render_template('document_detail.html', document=document, username=username)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    ensure_uploads_directory_exists()
    app.run(debug=False)
