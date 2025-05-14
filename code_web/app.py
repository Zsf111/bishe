from config import app
from models import User, House, db
from flask import request, jsonify, render_template, session
from datetime import datetime

from blueprints.auth import auth
from blueprints.user import user
from blueprints.house import house
from blueprints.graph import graph
from blueprints.recommend import recommend
from blueprints.admin_auth import admin_auth
from blueprints.admin import admin

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(house)
app.register_blueprint(graph)
app.register_blueprint(recommend)
app.register_blueprint(admin_auth)
app.register_blueprint(admin)

@app.context_processor
def inject_user():
    if session.get('user_id'):
        user = db.session.get(User, session['user_id'])
        return dict(user=user)
    return dict(user=None)

@app.route('/')
def index():
    # 随机获取5条房源数据
    random_houses = House.query.order_by().limit(5).all()
    
    if session.get('user_id'):
        user = db.session.get(User, session['user_id'])
        return render_template('home.html', user=user, houses=random_houses)
    else:
        return render_template('home.html', houses=random_houses)

if __name__ == '__main__':
    app.run(debug=True)