from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

app.config['SQLALCHEMY_DATABASE_URI'] = '数据库信息'
# app.config['JSON_AS_ASCII'] = False
