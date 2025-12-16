from app import app, db, Question

with app.app_context():
    print("=== 检查题目数据格式 ===")
    
    all_questions = Question.query.all()
    problematic_questions = []
    
    for i, q in enumerate(all_questions, 1):
        try:
            # 尝试解析options
            if q.options:
                import json
                options = json.loads(q.options)
                print(f"✅ 题目{i}: 选项格式正确")
            else:
                print(f"⚠️  题目{i}: 选项为空")
                problematic_questions.append(i)
        except Exception as e:
            print(f"❌ 题目{i}: 选项格式错误 - {str(e)}")
            problematic_questions.append(i)
            print(f"   原始选项数据: {repr(q.options)}")
    
    print(f"\n=== 检查结果 ===")
    print(f"总题目数: {len(all_questions)}")
    print(f"格式有问题的题目数: {len(problematic_questions)}")
    
    if problematic_questions:
        print(f"有问题的题目ID: {problematic_questions}")
    else:
        print("✅ 所有题目的选项格式都正确")
    
    # 查看前几道题目的详细数据
    print("\n=== 部分题目数据预览 ===")
    for q in all_questions[:3]:
        print(f"\n题目ID: {q.id}")
        print(f"题目类型: {q.question_type}")
        print(f"原始选项: {repr(q.options)}")
        print(f"原始答案: {repr(q.correct_answer)}")