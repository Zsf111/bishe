from models import User, House, db
from flask import request, jsonify, session, Blueprint, redirect, render_template, url_for

house = Blueprint('house', __name__, url_prefix='/house')

@house.route('/<int:house_id>/favorite', methods=['POST'])
def favorite_house(house_id):
    try:
        # 检查用户是否登录
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
            
        # 获取用户和房屋
        user = db.session.get(User, user_id)
        house = db.session.get(House, house_id)
        
        if not user or not house:
            return jsonify({'error': '数据不存在'}), 404
            
        # 切换收藏状态
        if house in user.favorite_houses:
            user.favorite_houses.remove(house)
            status = 'removed'
        else:
            user.favorite_houses.append(house)
            status = 'added'
            
        db.session.commit()
        return jsonify({'status': status}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@house.route('/<int:house_id>', methods=['GET'])
def show_house(house_id):
    try:
        # 获取指定id的房屋详细信息
        house = db.session.get(House, house_id)
        if not house:
            return jsonify({'error': '房源不存在'}), 404
        
        # 获取当前用户（如果已登录）
        user = None
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
            # 记录浏览历史
            if user and house not in user.viewed_houses:
                user.viewed_houses.append(house)
                db.session.commit()
        
        return render_template('house.html', house=house, user=user)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@house.route('/list')
def house_list():
    page = request.args.get('page', 1, type=int)
    per_page = 8  # 每页显示8个房源
    max_pages = 100  # 最大显示100页
    
    # 构建查询
    query = House.query
    
    # 添加关键词搜索
    keyword = request.args.get('keyword')
    if keyword:
        query = query.filter(House.community_name.ilike(f'%{keyword}%'))
    
    # 添加筛选条件
    if request.args.get('min_total_price'):
        query = query.filter(House.total_price >= float(request.args.get('min_total_price')))
    if request.args.get('max_total_price'):
        query = query.filter(House.total_price <= float(request.args.get('max_total_price')))
    if request.args.get('district'):
        query = query.filter(House.district == request.args.get('district'))
    if request.args.get('min_area'):
        query = query.filter(House.house_area >= float(request.args.get('min_area')))
    if request.args.get('max_area'):
        query = query.filter(House.house_area <= float(request.args.get('max_area')))
    if request.args.get('house_type'):
        query = query.filter(House.house_type == request.args.get('house_type'))
    
    # 获取总数并限制最大页数
    total = min(query.count(), max_pages * per_page)
    total_pages = min((total + per_page - 1) // per_page, max_pages)
    
    # 如果当前页超出范围，重定向到第一页
    if page > total_pages:
        return redirect(url_for('house.house_list', page=1))
    
    # 获取当前页的数据
    houses = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # 获取所有可选的区域和户型，用于筛选
    def get_districts():
        districts = db.session.query(House.district).distinct().all()
        return [d[0] for d in districts if d[0]]  # 过滤掉空值并获取第一个元素
        
    def get_house_types():
        house_types = db.session.query(House.house_type).distinct().all()
        return [t[0] for t in house_types if t[0]]  # 过滤掉空值并获取第一个元素

    return render_template('house_list.html',
                         houses=houses,
                         current_page=page,
                         total_pages=total_pages,
                         districts=get_districts(),  # 获取所有区域
                         house_types=get_house_types())  # 获取所有户型
