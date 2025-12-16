from app import app, db, Question

with app.app_context():
    # 查询所有不同的subject值
    subjects = db.session.query(Question.subject).distinct().all()
    print("数据库中的subject值:")
    for subject in subjects:
        print(f"  '{subject[0]}' (长度: {len(subject[0])})")
    
    # 查询马克思主义相关题目的数量
    marx_questions = Question.query.filter(Question.subject.like('%马克思%')).all()
    print(f"\n包含'马克思'的题目数量: {len(marx_questions)}")
    
    if marx_questions:
        print(f"第一个马克思主义题目的subject值: '{marx_questions[0].subject}'")