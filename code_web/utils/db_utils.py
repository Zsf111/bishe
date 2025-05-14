from functools import wraps
from flask import jsonify
from models import db

def transaction(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return decorated_function