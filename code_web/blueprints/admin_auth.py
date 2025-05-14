from flask import Blueprint, request, jsonify, session, render_template, redirect
from models import Admin, db
from datetime import datetime
from utils.db_utils import transaction

admin_auth = Blueprint('admin_auth', __name__, url_prefix='/admin/auth')

@admin_auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({'error': '用户名和密码不能为空'}), 400

            admin = Admin.query.filter_by(username=username).first()
            
            if admin and password == admin.password:
                session['admin_id'] = admin.admin_id
                admin.last_login = datetime.now()
                db.session.commit()
                return jsonify({'message': '登录成功'}), 200
            else:
                return jsonify({'error': '用户名或密码错误'}), 401

        return render_template('admin/login.html')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_auth.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect('/admin/auth/login')