import os
import sys
import sqlite3

# 添加项目目录到路径
sys.path.append('d:\\新建文件夹')

# 数据库路径
db_path = 'd:\\新建文件夹\\exam_system.db'

def check_questions():
    """检查数据库中的题目数据"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查看所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("数据库中的表:")
    for table in tables:
        print(f"- {table[0]}")
    
    # 查看题目总数
    cursor.execute("SELECT COUNT(*) FROM questions;")
    total_questions = cursor.fetchone()[0]
    print(f"\n总题目数: {total_questions}")
    
    # 查看马克思主义基本原理的题目
    cursor.execute("SELECT COUNT(*) FROM questions WHERE subject='马克思主义基本原理';")
    marx_questions = cursor.fetchone()[0]
    print(f"马克思主义基本原理题目数: {marx_questions}")
    
    # 查看其他科目
    cursor.execute("SELECT subject, COUNT(*) FROM questions GROUP BY subject;")
    subjects = cursor.fetchall()
    print("\n各科目题目分布:")
    for subject, count in subjects:
        print(f"- {subject}: {count}")
    
    # 查看题目类型分布
    cursor.execute("SELECT question_type, COUNT(*) FROM questions GROUP BY question_type;")
    question_types = cursor.fetchall()
    print("\n题目类型分布:")
    for qtype, count in question_types:
        print(f"- {qtype}: {count}")
    
    # 查看部分马克思主义题目示例
    cursor.execute("SELECT question_text, question_type, options, correct_answer, difficulty FROM questions WHERE subject='马克思主义基本原理' LIMIT 3;")
    sample_questions = cursor.fetchall()
    print("\n马克思主义题目示例:")
    for i, (qtext, qtype, options, correct, difficulty) in enumerate(sample_questions, 1):
        print(f"\n{i}. {qtext[:100]}...")
        print(f"   类型: {qtype}, 难度: {difficulty}")
        print(f"   选项: {options[:100]}...")
        print(f"   答案: {correct}")
    
    conn.close()

if __name__ == "__main__":
    check_questions()
