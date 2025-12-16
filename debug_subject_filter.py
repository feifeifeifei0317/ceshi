from app import app, db, Question

with app.app_context():
    # 直接查询所有题目
    all_questions = Question.query.all()
    print(f"总题目数: {len(all_questions)}")
    
    # 直接检查subject字段
    subject_to_test = "马克思主义基本原理"
    print(f"\n测试subject: '{subject_to_test}'")
    
    # 方法1: 使用filter_by
    filtered_by_subject = Question.query.filter_by(subject=subject_to_test).all()
    print(f"方法1 - filter_by结果: {len(filtered_by_subject)}道题")
    
    # 方法2: 使用filter和==
    filtered_by_equals = Question.query.filter(Question.subject == subject_to_test).all()
    print(f"方法2 - filter == 结果: {len(filtered_by_equals)}道题")
    
    # 方法3: 使用like
    filtered_by_like = Question.query.filter(Question.subject.like('%马克思%')).all()
    print(f"方法3 - filter like 结果: {len(filtered_by_like)}道题")
    
    # 检查一些题目
    print("\n题目示例:")
    for q in all_questions[:3]:
        print(f"  ID: {q.id}, Subject: '{q.subject}', 匹配: {q.subject == subject_to_test}")
        print(f"    题目: {q.question_text[:50]}...")