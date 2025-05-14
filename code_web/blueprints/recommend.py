from flask import Blueprint, render_template, session, redirect
from models import User, House, db
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd

recommend = Blueprint('recommend', __name__, url_prefix='/recommend')

def prepare_data():
    """准备训练数据"""
    houses = House.query.all()
    
    # 创建特征编码器
    le_district = LabelEncoder()
    le_orient = LabelEncoder()
    le_type = LabelEncoder()
    le_renov = LabelEncoder()
    
    # 准备数据
    data = {
        'district': [h.district for h in houses],
        'house_area': [h.house_area for h in houses],
        'house_orient': [h.house_orient for h in houses],
        'house_type': [h.house_type for h in houses],
        'renov_condi': [h.renov_condi for h in houses],
        'total_price': [h.total_price for h in houses]
    }
    
    # 转换为DataFrame
    df = pd.DataFrame(data)
    
    # 处理缺失值并编码特征
    df['house_area'] = df['house_area'].fillna(df['house_area'].mean())
    df['house_orient'] = df['house_orient'].fillna('未知')
    df['house_type'] = df['house_type'].fillna('未知')
    df['renov_condi'] = df['renov_condi'].fillna('未知')
    
    # 编码分类特征
    df['district_encoded'] = le_district.fit_transform(df['district'])
    df['orient_encoded'] = le_orient.fit_transform(df['house_orient'])
    df['type_encoded'] = le_type.fit_transform(df['house_type'])
    df['renov_encoded'] = le_renov.fit_transform(df['renov_condi'])
    
    return df, houses, (le_district, le_orient, le_type, le_renov)

def train_model(df):
    """训练决策树模型"""
    # 定义特征列名
    feature_columns = ['district_encoded', 'house_area', 'orient_encoded', 
                      'type_encoded', 'renov_encoded', 'total_price']
    
    X = df[feature_columns]  # 使用命名的特征列
    y = df['total_price']
    
    model = DecisionTreeRegressor(max_depth=5, random_state=42)
    model.fit(X, y)
    
    return model, feature_columns  # 返回模型和特征列名

def get_user_preferences(user_id):
    """获取用户偏好"""
    user = db.session.get(User, user_id)
    if not user or not user.favorite_houses:
        return None
    
    # 从用户收藏的房源中提取偏好
    favorites = user.favorite_houses
    preferences = {
        'district': max(set([h.district for h in favorites]), key=lambda x: [h.district for h in favorites].count(x)),
        'house_area': sum([h.house_area for h in favorites]) / len(favorites),
        'house_orient': max(set([h.house_orient for h in favorites]), key=lambda x: [h.house_orient for h in favorites].count(x)),
        'house_type': max(set([h.house_type for h in favorites]), key=lambda x: [h.house_type for h in favorites].count(x)),
        'renov_condi': max(set([h.renov_condi for h in favorites]), key=lambda x: [h.renov_condi for h in favorites].count(x)),
        'total_price': sum([h.total_price for h in favorites]) / len(favorites)
    }
    
    return preferences

@recommend.route('/')
def show_recommendations():
    """显示推荐房源"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/auth/login')
    
    try:
        # 准备数据
        df, houses, encoders = prepare_data()
        le_district, le_orient, le_type, le_renov = encoders
        
        # 获取用户偏好
        preferences = get_user_preferences(user_id)
        
        if not preferences:
            # 用户没有收藏，返回随机推荐
            recommended_houses = House.query.order_by(db.func.random()).limit(6).distinct().all()
            return render_template('recommend.html', houses=recommended_houses, message="基于随机推荐")
        
        # 训练模型并获取特征列名
        model, feature_columns = train_model(df)
        
        # 计算每个房源的匹配度
        predictions = []
        seen_house_ids = set()
        
        for i, house in enumerate(houses):
            if house.house_id in seen_house_ids:
                continue
                
            try:
                # 准备房源特征
                house_features = pd.DataFrame([[
                    df.iloc[i]['district_encoded'],
                    df.iloc[i]['house_area'],
                    df.iloc[i]['orient_encoded'],
                    df.iloc[i]['type_encoded'],
                    df.iloc[i]['renov_encoded'],
                    df.iloc[i]['total_price']
                ]], columns=feature_columns)
                
                # 计算匹配度分数
                prediction = model.predict(house_features)[0]
                
                # 计算与用户偏好的价格差异
                price_diff = abs(house.total_price - preferences['total_price'])
                price_similarity = 1 / (1 + price_diff / preferences['total_price'])
                
                # 综合评分（结合模型预测和价格相似度）
                score = 0.7 * (1 / (1 + abs(prediction - preferences['total_price']))) + 0.3 * price_similarity
                
                predictions.append((house, score))
                seen_house_ids.add(house.house_id)
                
            except Exception as e:
                print(f"计算房源 {i} 的匹配度时出错: {str(e)}")
                continue
        
        # 选择最匹配的6个房源
        predictions.sort(key=lambda x: x[1], reverse=True)
        recommended_houses = [house for house, _ in predictions[:6]]
        
        # 如果推荐数量不足，补充随机房源
        if len(recommended_houses) < 6:
            seen_ids = {h.house_id for h in recommended_houses}
            random_houses = House.query.filter(
                ~House.house_id.in_(seen_ids)
            ).order_by(db.func.random()).limit(6 - len(recommended_houses)).all()
            recommended_houses.extend(random_houses)
        
        return render_template('recommend.html', 
                             houses=recommended_houses, 
                             message="基于您的收藏推荐")
        
    except Exception as e:
        print(f"推荐失败: {str(e)}")
        return render_template('recommend.html', error="推荐系统暂时无法使用")
