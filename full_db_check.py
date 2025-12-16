from app import app, db, Exam, Question
import json

with app.app_context():
    print("=== 数据库完整性检查 ===")
    
    # 1. 检查题目表
    total_questions = Question.query.count()
    print(f"\n1. 题目总数: {total_questions}")
    
    # 按科目分类统计
    subjects = db.session.query(Question.subject).distinct().all()
    subjects = [sub[0] for sub in subjects]
    
    for subject in subjects:
        count = Question.query.filter_by(subject=subject).count()
        print(f"   - {subject}: {count}道题")
    
    # 2. 检查考试表
    total_exams = Exam.query.count()
    print(f"\n2. 考试总数: {total_exams}")
    
    active_exams = Exam.query.filter_by(is_active=True).count()
    print(f"   - 活跃考试: {active_exams}")
    
    if total_exams > 0:
        print("\n   考试详情:")
        exams = Exam.query.all()
        for exam in exams:
            # 解析题目ID列表
            question_ids = json.loads(exam.question_ids) if exam.question_ids else []
            
            # 检查考试中的题目是否都存在
            invalid_ids = []
            for qid in question_ids:
                if not Question.query.get(qid):
                    invalid_ids.append(qid)
            
            status = "✅ 正常" if not invalid_ids else f"❌ 有{len(invalid_ids)}道无效题目"
            print(f"   - ID:{exam.id} '{exam.title}' [{exam.time_limit}分钟]: {len(question_ids)}道题 {status}")
            
            if invalid_ids:
                print(f"     无效题目ID: {invalid_ids}")
    
    # 3. 检查马克思主义题目详情
    marx_questions = Question.query.filter_by(subject='马克思主义基本原理').all()
    if marx_questions:
        print(f"\n3. 马克思主义基本原理题目抽样:")
        # 显示前3道题目的基本信息
        for i, q in enumerate(marx_questions[:3], 1):
            print(f"   - 第{i}题: {q.question_text[:50]}... (难度: {q.difficulty})")
            # 处理options - 支持Python列表格式和JSON格式
            try:
                options = json.loads(q.options)
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试eval（仅用于已知安全的Python列表格式）
                import ast
                options = ast.literal_eval(q.options)
            print(f"     选项: {', '.join(options[:3])}...")
    
    print("\n=== 检查完成 ===")