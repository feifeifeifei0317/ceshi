import requests
import json

def test_api_endpoints():
    base_url = 'http://localhost:5000'
    
    print('=== 测试API端点 ===')
    
    # 测试1: 获取考试列表
    print('\n1. 测试GET /api/exams')
    try:
        response = requests.get(f'{base_url}/api/exams')
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            exams = response.json()
            print(f'返回考试数量: {len(exams)}')
            for exam in exams[:3]:  # 只显示前3个
                print(f'  考试ID: {exam["id"]}, 标题: {exam["title"]}')
    except Exception as e:
        print(f'错误: {e}')
    
    # 测试2: 获取特定考试
    print('\n2. 测试GET /api/exam/1')
    try:
        response = requests.get(f'{base_url}/api/exam/1')
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            exam = response.json()
            print(f'考试标题: {exam["title"]}')
            print(f'题目数量: {len(exam["questions"])}')
    except Exception as e:
        print(f'错误: {e}')
    
    # 测试3: 测试题目过滤功能
    print('\n3. 测试GET /api/questions?subject=马克思')
    try:
        response = requests.get(f'{base_url}/api/questions', params={'subject': '马克思'})
        print(f'状态码: {response.status_code}')
        if response.status_code == 200:
            questions = response.json()
            print(f'返回题目数量: {len(questions)}')
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n=== API测试完成 ===')

if __name__ == '__main__':
    test_api_endpoints()
