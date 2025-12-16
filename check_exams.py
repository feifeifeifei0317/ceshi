from app import app, db, Exam

with app.app_context():
    # 检查是否有考试数据
    exams = Exam.query.all()
    print(f"数据库中共有 {len(exams)} 个考试")
    
    if exams:
        print("考试列表：")
        for exam in exams:
            print(f"- ID: {exam.id}, 标题: {exam.title}, 科目: {exam.subject}, 活跃: {exam.is_active}")
    else:
        print("数据库中没有考试数据")
        
    # 同时检查题目表中是否有马克思主义题目
    from app import Question
    marx_questions = Question.query.filter_by(subject='马克思主义基本原理').all()
    print(f"\n马克思主义基本原理题目数量：{len(marx_questions)}")