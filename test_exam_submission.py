import requests
import json

def test_exam_submission():
    base_url = 'http://localhost:5000'
    
    print('=== 测试考试提交流程 ===')
    
    # 获取最新创建的考试ID
    print('\n1. 获取最新的考试')
    try:
        exams_response = requests.get(f'{base_url}/api/exams')
        exams = exams_response.json()
        # 找到最新的考试（按ID排序）
        latest_exam = sorted(exams, key=lambda x: x['id'], reverse=True)[0]
        exam_id = latest_exam['id']
        print(f'最新考试ID: {exam_id}, 标题: {latest_exam["title"]}')
        
        # 获取考试详细信息
        exam_response = requests.get(f'{base_url}/api/exam/{exam_id}')
        exam = exam_response.json()
        print(f'考试题目数量: {len(exam["questions"])}')
        
        # 准备答案数据
        print('\n2. 准备考试答案')
        answers = {}
        for question in exam['questions']:
            qid = str(question['id'])
            # 根据题目类型生成答案
            if question['question_type'] in ['single_choice', 'true_false']:
                # 单选题和判断题：选择第一个选项
                answers[qid] = [0]  # 假设选项索引从0开始
            elif question['question_type'] == 'multiple_choice':
                # 多选题：选择前两个选项
                answers[qid] = [0, 1]
            elif question['question_type'] == 'fill_blank':
                # 填空题：简单填写内容
                answers[qid] = ['测试答案']
        
        print(f'生成的答案: {answers}')
        
        # 提交考试
        print('\n3. 提交考试')
        submission_data = {
            'exam_id': exam_id,
            'student_name': '测试学生',
            'answers': answers,
            'time_taken': 1200  # 20分钟
        }
        
        submission_response = requests.post(f'{base_url}/api/submit_exam', json=submission_data)
        print(f'状态码: {submission_response.status_code}')
        result = submission_response.json()
        print(f'响应: {result}')
        
        if result['success']:
            submission_id = result['submission_id']
            print(f'\n4. 获取考试结果')
            result_response = requests.get(f'{base_url}/api/result/{submission_id}')
            print(f'状态码: {result_response.status_code}')
            if result_response.status_code == 200:
                result_data = result_response.json()
                print(f'考试得分: {result_data["score"]}/{result_data["total_score"]}')
                print(f'用时: {result_data["time_taken"]}秒')
                
                # 显示部分答题结果
                print('\n5. 答题结果摘要')
                for i, question_result in enumerate(result_data["detailed_results"][:2]):
                    print(f'\n题目{i+1}:')
                    print(f'   得分: {question_result["score"]}')
                    print(f'   是否正确: {"是" if question_result["is_correct"] else "否"}')
                    print(f'   用户答案: {question_result["user_answer"]}')
                    print(f'   正确答案: {question_result["correct_answer"]}')
    except Exception as e:
        print(f'错误: {e}')
    
    print('\n=== 考试提交流程测试完成 ===')

if __name__ == '__main__':
    test_exam_submission()
