from app import app, db, Question, Exam
import random
import json

# 模拟create_exam函数的逻辑
def simulate_create_exam(title="测试考试", description="", question_count=5, difficulty=None, subject=None, total_score=100, time_limit=60):
    with app.app_context():
        try:
            print(f"模拟创建考试: {title}")
            print(f"参数: subject='{subject}', difficulty='{difficulty}', question_count={question_count}")
            
            # 随机生成题目
            query = Question.query
            if difficulty:
                query = query.filter_by(difficulty=difficulty)
                print(f"应用difficulty过滤: '{difficulty}'")
            if subject:
                query = query.filter_by(subject=subject)
                print(f"应用subject过滤: '{subject}'")
            
            available_questions = query.all()
            print(f"过滤后可用题目数: {len(available_questions)}")
            
            if len(available_questions) < question_count:
                return {'success': False, 'message': f'可用题目不足，只有{len(available_questions)}道题'}
            
            selected_questions = random.sample(available_questions, question_count)
            question_ids = [q.id for q in selected_questions]
            print(f"选中的题目ID: {question_ids}")
            
            # 创建考试
            exam = Exam(
                title=title,
                description=description,
                question_ids=json.dumps(question_ids),
                total_score=total_score,
                time_limit=time_limit
            )
            
            db.session.add(exam)
            db.session.commit()
            
            return {'success': True, 'exam_id': exam.id, 'message': '考试创建成功'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

# 测试
def run_tests():
    # 测试1: 不指定subject
    print("\n=== 测试1: 不指定subject ===")
    result1 = simulate_create_exam(title="测试考试1", question_count=5)
    print(result1)
    
    # 测试2: 指定subject
    print("\n=== 测试2: 指定subject ===")
    result2 = simulate_create_exam(title="测试考试2", question_count=5, subject="马克思主义基本原理")
    print(result2)
    
    # 测试3: 使用不同的question_count
    print("\n=== 测试3: 使用不同的question_count ===")
    result3 = simulate_create_exam(title="测试考试3", question_count=10, subject="马克思主义基本原理")
    print(result3)

if __name__ == "__main__":
    run_tests()