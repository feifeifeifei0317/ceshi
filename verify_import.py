import sys
import os

# 切换到项目根目录
os.chdir('d:\\新建文件夹')

# 添加项目根目录到系统路径
sys.path.append('.')

from flask import Flask
from models import db, Question

# 创建Flask应用实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

with app.app_context():
    # 创建数据库表
    db.create_all()
    
    # 查询马克思主义基本原理题目的数量
    marx_questions_count = Question.query.filter_by(subject='马克思主义基本原理').count()
    print(f"数据库中马克思主义基本原理题目总数: {marx_questions_count} 道")
    
    # 查询所有题目的总数，确认导入前后的变化
    all_questions_count = Question.query.count()
    print(f"数据库中所有题目总数: {all_questions_count} 道")
