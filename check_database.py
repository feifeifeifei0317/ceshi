from app import app, db, Question, Exam

with app.app_context():
    print('--- 题目数据统计 ---')
    total_questions = Question.query.count()
    marx_questions = Question.query.filter(Question.subject.like('%马克思%')).count()
    print(f'总题目数: {total_questions}')
    print(f'马克思主义题目数: {marx_questions}')
    
    print('\n--- 考试数据统计 ---')
    total_exams = Exam.query.count()
    print(f'总考试数: {total_exams}')
    
    # 显示前3个考试的基本信息
    exams = Exam.query.limit(3).all()
    if exams:
        print('\n前3个考试信息:')
        for exam in exams:
            print(f'  考试ID: {exam.id}, 标题: {exam.title}, 题目数量: {len(exam.question_ids)}')
    
    # 显示数据库路径
    print('\n--- 数据库配置 ---')
    print(f'数据库URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    print('\n数据库检查完成')
