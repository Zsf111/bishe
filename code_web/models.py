from config import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

# 收藏关系表（多对多）
favorite = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('house.house_id'), primary_key=True),
    db.Column('favorite_time', db.DateTime, nullable=False, default=datetime.now)
)

# 浏览记录表（多对多）
history = db.Table('history',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('house.house_id'), primary_key=True),
    db.Column('view_time', db.DateTime, nullable=False, default=datetime.now)
)

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    profile = db.Column(db.Text)

    # 关系定义
    favorite_houses = db.relationship('House', 
                                    secondary=favorite,
                                    backref=db.backref('favorited_by', lazy='dynamic'))
    viewed_houses = db.relationship('House',
                                  secondary=history,
                                  backref=db.backref('viewed_by', lazy='dynamic'))

class House(db.Model):
    __tablename__ = 'house'
    
    house_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    community_name = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(5), nullable=False)
    sub_district = db.Column(db.String(5))
    total_price = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    house_type = db.Column(db.String(5))
    house_area = db.Column(db.Float)
    house_struc = db.Column(db.String(5))
    const_type = db.Column(db.String(5))
    house_floor = db.Column(db.Integer)
    house_orient = db.Column(db.String(5))
    const_struc = db.Column(db.String(5))
    renov_condi = db.Column(db.String(5))
    lift_rate = db.Column(db.String(5))
    heat_method = db.Column(db.String(5))
    have_lift = db.Column(db.Boolean, default=False)
    trans_owner = db.Column(db.String(5))
    house_purpo = db.Column(db.String(5))
    house_age = db.Column(db.String(5))
    prope_owner = db.Column(db.String(5))
    mortg_info = db.Column(db.String(50))


class Admin(db.Model):
    __tablename__ = 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime)
    