import requests
import json

def test_exam_creation():
    base_url = 'http://localhost:5000'
    
    print('=== 测试考试创建流程 ===')
    
    # 测试1: 创建马克思主义基本原理考试
    print('\n1. 测试创建马克思主义基本原理考试')
    exam_data = {
        'title': '马克思主义基本原理测试',
        'description': '测试用马克思主义基本原理考试',
        'question_count': 5,
        'subject': '马克思主义基本原理',
        'total_score': 50,
        'time_limit': 30
    }
    
    try:
        response = requests.post(f'{base_url}/api/create_exam', json=exam_data)
        print(f'状态码: {response.status_code}')
        result = response.json()
        print(f'响应: {result}')
        
        if result['success']:
            exam_id = result['exam_id']
            print(f'\n2. 验证新创建的考试')
            exam_response = requests.get(f'{base_url}/api/exam/{exam_id}')
            print(f'状态码: {exam_response.status_code}')
            if exam_response.status_code == 200:
                exam = exam_response.json()
                print(f'考试标题: {exam["title"]}')
                print(f'题目数量: {len(exam["questions"])}')
                print(f'考试时间: {exam["time_limit"]}分钟')
                
                # 验证题目都是马克思主义相关的
                print('\n3. 验证考试题目内容')
                for i, question in enumerate(exam["questions"][:2]):  # 只显示前2道
                    print(f'\n题目{i+1}: {question["question_text"]}')
                    print(f'   类型: {question["question_type"]}')
                    print(f'   科目: {question["subject"]}')
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n=== 考试创建流程测试完成 ===')

if __name__ == '__main__':
    test_exam_creation()
