import requests

try:
    response = requests.get('http://localhost:5000/api/exams')
    print(f'Flask应用状态: {response.status_code}')
    print('考试列表数据:', response.json())
except Exception as e:
    print(f'Flask应用未运行或出现错误: {e}')
