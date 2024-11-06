from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 更新数据库配置，指向已有的数据库文件
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 确保路径指向你已有的数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 创建数据库表（如果数据库已存在，则无需此操作，但可以保持以防万一）
# with app.app_context():
#     db.create_all()

# 首页路由，显示所有用户
@app.route('/')
def index():
    users = User.query.all()  # 获取所有用户
    return render_template('index.html', users=users)

# 添加用户路由
@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
