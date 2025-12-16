from app import app, db, Exam, Question
import random

with app.app_context():
    # 查询所有马克思主义基本原理的题目
    marx_questions = Question.query.filter_by(subject='马克思主义基本原理').all()
    
    if not marx_questions:
        print("错误：数据库中没有马克思主义基本原理的题目！")
        exit(1)
    
    print(f"找到 {len(marx_questions)} 道马克思主义基本原理题目")
    
    # 随机选择20道题目用于考试
    selected_questions = random.sample(marx_questions, min(20, len(marx_questions)))
    question_ids = [q.id for q in selected_questions]
    
    # 创建新的马克思主义基本原理测试考试
    new_exam = Exam(
        title="马克思主义基本原理测试",
        description="马克思主义基本原理知识测试",
        question_ids=str(question_ids),
        time_limit=60,  # 60分钟
        total_score=100,  # 总分100分
        is_active=True
    )
    
    # 保存到数据库
    db.session.add(new_exam)
    db.session.commit()
    
    print(f"\n成功创建考试！")
    print(f"考试ID: {new_exam.id}")
    print(f"考试标题: {new_exam.title}")
    print(f"题目数量: {len(selected_questions)}")
    print(f"时间限制: {new_exam.time_limit}分钟")
    print(f"是否活跃: {new_exam.is_active}")
    print(f"\n考试已成功创建并激活，现在可以参加测试了！")