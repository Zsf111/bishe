from models import User, db, House, history
from flask import request, jsonify, session, Blueprint, redirect, render_template
import bcrypt
from datetime import datetime

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<int:user_id>')
def show_user(user_id):
    print(f"Accessing user {user_id}")  # 添加调试输出
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@user.route('/edit', methods=['GET', 'POST'])
def edit_user():
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
            username = data.get('username')
            profile = data.get('profile')
            
            # 如果要修改用户名，需要检查新用户名是否已存在
            if username and username != user.username:
                if User.query.filter_by(username=username).first():
                    return jsonify({'error': '用户名已存在'}), 400
                user.username = username
                
            # 更新个人简介
            if profile is not None:
                user.profile = profile
                
            # 提交更改到数据库
            db.session.commit()
            
            return jsonify({
                'message': '更新成功',
                'username': user.username,
                'profile': user.profile
            }), 200
            
        # GET请求返回当前用户信息
        return render_template('user_edit.html', user=user)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@user.route('/history')
def user_history():
    try:
        # 检查用户是否登录
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')  # 未登录重定向到登录页
            
        # 获取用户及其浏览历史
        user = User.query.get_or_404(user_id)
        
        # 直接从数据库查询带时间戳的浏览记录
        viewed_houses = db.session.query(House, db.func.max(history.c.view_time).label('view_time'))\
            .join(history, House.house_id == history.c.house_id)\
            .filter(history.c.user_id == user_id)\
            .group_by(House)\
            .order_by(db.desc('view_time'))\
            .all()
        
        # 只取房屋对象
        user.viewed_houses = [house for house, _ in viewed_houses]
        
        return render_template('history.html', user=user)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user.route('/history/<int:house_id>', methods=['DELETE'])
def delete_history(house_id):
    try:
        # 检查用户是否登录
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
            
        # 获取用户和房屋
        user = User.query.get(user_id)
        house = House.query.get_or_404(house_id)
        
        if not user or not house:
            return jsonify({'error': '数据不存在'}), 404
            
        # 从浏览历史中移除
        if house in user.viewed_houses:
            user.viewed_houses.remove(house)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': '记录不存在'}), 404
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500