from models import User, db
from flask import request, jsonify, session, Blueprint, redirect, render_template
import bcrypt, re
from datetime import datetime

# 添加事务回滚
from utils.db_utils import transaction

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
@transaction
def register():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
        
            # 检查用户名是否为空
            if username == '':
                return jsonify({'error': '用户名不能为空'}), 400
            
            # 检查密码是否为空
            if password == '':
                return jsonify({'error': '密码不能为空'}), 400
            
            # 检查邮箱是否为空
            if email == '':
                return jsonify({'error': '邮箱不能为空'}), 400
            
            # 检查邮箱格式是否正确
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({'error': '请输入正确的邮箱格式'}), 400
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                return jsonify({'error': '用户名已存在'}), 400
            
            # 检查邮箱是否已存在
            if User.query.filter_by(email=email).first():
                return jsonify({'error': '邮箱已存在'}), 400

            # 生成密码哈希
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # 创建新用户
            new_user = User(
                username=username,
                password=hashed_password.decode('utf-8'),
                email=email,
                register_time=datetime.now()
            )
            
            # 添加到数据库
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({'message': '注册成功'}), 201
        return render_template('register.html')
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # 判定用户名是否为空
            if username == '':
                return jsonify({'error': '用户名不能为空'}), 400
            
            # 判定密码是否为空
            if password == '':
                return jsonify({'error': '密码不能为空'}), 400
            
            # 查询用户
            user = User.query.filter_by(username=username).first()
        
            if user and bcrypt.checkpw(password.encode('utf-8'), 
                                    user.password.encode('utf-8')):
                session['user_id'] = user.user_id
                return jsonify({'message': '登录成功'}), 200
            else:
                return jsonify({'error': '用户名或密码错误'}), 401
        return render_template('login.html')
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    try:
        # 检查用户是否登录
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
            
        # 获取当前用户
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        if request.method == 'POST':
            data = request.get_json()
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            
            # 验证旧密码是否正确
            if not bcrypt.checkpw(old_password.encode('utf-8'), 
                                user.password.encode('utf-8')):
                return jsonify({'error': '原密码错误'}), 401
            
            # 生成新密码哈希
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # 更新用户密码
            user.password = hashed_password.decode('utf-8')
            db.session.commit()
            session.pop('user_id')
            
            
            return jsonify({'message': '密码修改成功'}), 200
            
        # GET请求返回重置密码页面
        return render_template('reset.html', user=user)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@auth.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id')
    return redirect('/')