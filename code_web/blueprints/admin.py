from flask import Blueprint, render_template, jsonify, session, request
from models import Admin, User, House, db, history
from functools import wraps
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_id'):
            return jsonify({'error': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    try:
        # 获取当前管理员信息
        admin_id = session.get('admin_id')
        current_admin = Admin.query.get(admin_id)
        
        # 获取用户总数和房源总数
        user_count = User.query.count()
        house_count = House.query.count()
        
        # 获取今日访问量（从history表统计）
        today = datetime.now().date()
        daily_visits = db.session.query(history).filter(
            db.func.date(history.c.view_time) == today
        ).count()
        
        # 获取最新注册的用户
        latest_users = User.query.order_by(User.register_time.desc()).limit(5).all()
        
        # 获取最新添加的房源
        latest_houses = House.query.order_by(House.house_id.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
                             current_admin=current_admin,
                             user_count=user_count,
                             house_count=house_count,
                             daily_visits=daily_visits,
                             latest_users=latest_users,
                             latest_houses=latest_houses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/users')
@admin_required
def manage_users():
    try:
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/houses')
@admin_required
def manage_houses():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10  # 每页显示10个房源
        max_pages = 100  # 最大显示100页
        
        # 构建查询
        query = House.query
        
        # 添加关键词搜索
        keyword = request.args.get('keyword')
        if keyword:
            query = query.filter(House.community_name.ilike(f'%{keyword}%'))
        
        # 获取总数并限制最大页数
        total = min(query.count(), max_pages * per_page)
        total_pages = min((total + per_page - 1) // per_page, max_pages)
        
        # 获取当前页的数据
        houses = query.order_by(House.house_id.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        return render_template('admin/houses.html',
                             houses=houses,
                             current_page=page,
                             total_pages=total_pages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/houses', methods=['POST'])
@admin_required
def add_house():
    try:
        data = request.get_json()
        
        # 必填字段验证
        required_fields = ['community_name', 'district', 'total_price', 'unit_price', 'house_type', 'house_area']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field}不能为空'}), 400
        
        # 数据类型转换
        try:
            total_price = float(data['total_price'])
            unit_price = float(data['unit_price'])
            house_area = float(data['house_area'])
            house_floor = int(data['house_floor']) if data.get('house_floor') else None
            have_lift = data.get('have_lift') == 'true'
        except ValueError:
            return jsonify({'error': '数值字段格式错误'}), 400
        
        # 创建新房源
        new_house = House(
            community_name=data['community_name'],
            district=data['district'],
            sub_district=data.get('sub_district'),
            total_price=total_price,
            unit_price=unit_price,
            house_type=data['house_type'],
            house_area=house_area,
            house_struc=data.get('house_struc'),
            const_type=data.get('const_type'),
            house_floor=house_floor,
            house_orient=data.get('house_orient'),
            const_struc=data.get('const_struc'),
            renov_condi=data.get('renov_condi'),
            lift_rate=data.get('lift_rate'),
            heat_method=data.get('heat_method'),
            have_lift=have_lift,
            trans_owner=data.get('trans_owner'),
            house_purpo=data.get('house_purpo'),
            house_age=data.get('house_age'),
            prope_owner=data.get('prope_owner'),
            mortg_info=data.get('mortg_info')
        )
        
        db.session.add(new_house)
        db.session.commit()
        return jsonify({'message': '房源添加成功', 'house_id': new_house.house_id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin.route('/houses/<int:house_id>', methods=['DELETE'])
@admin_required
def delete_house(house_id):
    try:
        house = House.query.get_or_404(house_id)
        db.session.delete(house)
        db.session.commit()
        return jsonify({'message': '房源删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # 清理用户相关数据
        user.viewed_houses.clear()  # 清除浏览历史
        user.favorite_houses.clear()  # 清除收藏记录
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': '用户删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500