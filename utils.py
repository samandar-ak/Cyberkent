from flask import abort
from html import escape

ALLOWED_EXTENSIONS = {'png'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def custom_safe(input_string):
    
    allowed_tags = ['h1', 'h2', 'p']
    
    for tag in allowed_tags:
        input_string = input_string.replace(f"&lt;{tag}&gt;", "").replace(f"&lt;/{tag}&gt;", "")
    
    return input_string 



