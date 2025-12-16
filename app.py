from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zhixing-platform-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhixing_exam_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 数据库模型
class Question(db.Model):
    """题目模型"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'single_choice', 'multiple_choice', 'true_false', 'fill_blank'
    options = db.Column(db.Text, nullable=False)  # JSON格式存储选项
    correct_answer = db.Column(db.Text, nullable=False)  # JSON格式存储正确答案
    explanation = db.Column(db.Text, nullable=False)  # 题目解析
    difficulty = db.Column(db.String(10), default='medium')  # easy, medium, hard
    subject = db.Column(db.String(50), default='general')  # 科目
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典格式"""
        # 处理options - 支持Python列表格式和JSON格式
        try:
            options = json.loads(self.options)
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试eval（仅用于已知安全的Python列表格式）
            import ast
            options = ast.literal_eval(self.options)
        
        # 处理correct_answer - 支持Python列表格式和JSON格式
        try:
            correct_answer = json.loads(self.correct_answer)
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试eval（仅用于已知安全的Python列表格式）
            import ast
            correct_answer = ast.literal_eval(self.correct_answer)
        
        return {
            'id': self.id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': options,
            'correct_answer': correct_answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'subject': self.subject
        }

class Exam(db.Model):
    """考试模型"""
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    question_ids = db.Column(db.Text, nullable=False)  # JSON格式存储题目ID列表
    total_score = db.Column(db.Integer, default=100)
    time_limit = db.Column(db.Integer, default=60)  # 时间限制（分钟）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_questions(self):
        """获取考试的所有题目"""
        question_ids = json.loads(self.question_ids)
        return Question.query.filter(Question.id.in_(question_ids)).all()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'question_ids': json.loads(self.question_ids),
            'total_score': self.total_score,
            'time_limit': self.time_limit,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Submission(db.Model):
    """答题记录模型"""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON格式存储答案
    score = db.Column(db.Float, default=0.0)
    total_score = db.Column(db.Float, default=0.0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)  # 用时（秒）
    detailed_results = db.Column(db.Text)  # JSON格式存储详细批改结果
    
    def get_answers(self):
        """获取答案字典"""
        return json.loads(self.answers)
    
    def get_detailed_results(self):
        """获取详细批改结果"""
        if self.detailed_results:
            return json.loads(self.detailed_results)
        return {}

# 初始化数据库
def init_db():
    """创建数据库表"""
    with app.app_context():
        db.create_all()
        print("数据库表创建完成")

# 路由配置
@app.route('/')
def index():
    """智星平台统一入口"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """用户仪表盘"""
    return render_template('dashboard.html')

# 考试系统API
@app.route('/api/exams')
def get_exams():
    """获取所有考试"""
    exams = Exam.query.filter_by(is_active=True).all()
    return jsonify([exam.to_dict() for exam in exams])

@app.route('/api/questions')
def get_questions():
    """获取题库"""
    subject = request.args.get('subject')
    difficulty = request.args.get('difficulty')
    
    query = Question.query
    if subject:
        # 清理subject参数，移除可能的空格和不可见字符
        subject = subject.strip()
        # 尝试精确匹配
        filtered_by_exact = query.filter_by(subject=subject).all()
        if not filtered_by_exact:
            # 如果精确匹配失败，尝试模糊匹配
            query = query.filter(Question.subject.like(f'%{subject}%'))
        else:
            query = query.filter_by(subject=subject)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    questions = query.all()
    return jsonify([question.to_dict() for question in questions])

@app.route('/api/create_exam', methods=['POST'])
def create_exam():
    """创建考试"""
    data = request.get_json()
    title = data.get('title', '未命名考试')
    description = data.get('description', '')
    question_count = int(data.get('question_count', 10))
    difficulty = data.get('difficulty', None)
    # 清理subject参数，移除可能的空格和不可见字符
    subject = data.get('subject', None)
    if subject:
        subject = subject.strip()
    total_score = int(data.get('total_score', 100))
    time_limit = int(data.get('time_limit', 60))
    
    try:
        # 随机生成题目
        query = Question.query
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        if subject:
            # 尝试精确匹配
            filtered_by_exact = query.filter_by(subject=subject).all()
            if not filtered_by_exact:
                # 如果精确匹配失败，尝试模糊匹配
                query = query.filter(Question.subject.like(f'%{subject}%'))
            else:
                query = query.filter_by(subject=subject)
        
        available_questions = query.all()
        if len(available_questions) < question_count:
            return jsonify({'success': False, 'message': f'可用题目不足，只有{len(available_questions)}道题'})
        
        selected_questions = random.sample(available_questions, question_count)
        question_ids = [q.id for q in selected_questions]
        
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
        
        return jsonify({'success': True, 'exam_id': exam.id, 'message': '考试创建成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# 考试系统路由
@app.route('/exam/<int:exam_id>')
def take_exam(exam_id):
    """参加考试"""
    exam = Exam.query.get_or_404(exam_id)
    if not exam.is_active:
        return render_template('error.html', message='该考试已关闭')
    
    return render_template('take_exam.html', exam=exam)

@app.route('/api/exam/<int:exam_id>')
def get_exam(exam_id):
    """获取特定考试"""
    exam = Exam.query.get_or_404(exam_id)
    exam_dict = exam.to_dict()
    exam_dict['questions'] = [q.to_dict() for q in exam.get_questions()]
    return jsonify(exam_dict)

@app.route('/api/submit_exam', methods=['POST'])
def submit_exam():
    """提交考试"""
    data = request.get_json()
    exam_id = data.get('exam_id')
    student_name = data.get('student_name', '匿名')
    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)
    
    try:
        exam = Exam.query.get_or_404(exam_id)
        exam_questions = exam.get_questions()
        
        # 计算得分
        total_score = exam.total_score
        question_score = total_score / len(exam_questions)
        score = 0.0
        detailed_results = []
        
        for question in exam_questions:
            user_answer = answers.get(str(question.id), [])
            
            # 处理不同类型的题目
            is_correct = False
            # 处理正确答案格式 - 支持Python列表格式和JSON格式
            try:
                correct_answer = json.loads(question.correct_answer)
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试eval（仅用于已知安全的Python列表格式）
                import ast
                correct_answer = ast.literal_eval(question.correct_answer)
            
            # 处理选项格式 - 支持Python列表格式和JSON格式
            try:
                options = json.loads(question.options)
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试eval（仅用于已知安全的Python列表格式）
                import ast
                options = ast.literal_eval(question.options)
            
            # 转换用户答案为实际选项文本
            option_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            converted_user_answer = []
            
            if isinstance(options, list):
                # 数组格式选项，将用户选择的A/B/C转换为对应的选项文本
                for ans in user_answer:
                    index = option_labels.index(ans) if ans in option_labels else int(ans)
                    if 0 <= index < len(options):
                        converted_user_answer.append(options[index])
            else:
                # 对象格式选项，直接使用用户答案
                converted_user_answer = user_answer
            
            # 比较答案
            if question.question_type == 'true_false' or question.question_type == 'single_choice':
                # 单选题或判断题
                if converted_user_answer:
                    is_correct = str(converted_user_answer[0]) == str(correct_answer[0])
            elif question.question_type == 'multiple_choice':
                # 多选题
                is_correct = sorted(converted_user_answer) == sorted(correct_answer)
            
            if is_correct:
                score += question_score
            
            detailed_results.append({
                'question_id': question.id,
                'question_text': question.question_text,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'score': question_score if is_correct else 0,
                'explanation': question.explanation
            })
        
        # 创建答题记录
        submission = Submission(
            student_name=student_name,
            exam_id=exam_id,
            answers=json.dumps(answers),
            score=round(score, 2),
            total_score=total_score,
            time_taken=time_taken,
            detailed_results=json.dumps(detailed_results)
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '考试提交成功',
            'submission_id': submission.id,
            'score': submission.score,
            'total_score': submission.total_score,
            'detailed_results': submission.get_detailed_results()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/result/<int:submission_id>')
def view_result(submission_id):
    """查看考试结果"""
    submission = Submission.query.get_or_404(submission_id)
    exam = Exam.query.get_or_404(submission.exam_id)
    
    return render_template('result.html', submission=submission, exam=exam)

@app.route('/api/result/<int:submission_id>')
def get_result(submission_id):
    """获取考试结果"""
    submission = Submission.query.get_or_404(submission_id)
    exam = Exam.query.get_or_404(submission.exam_id)
    
    result = {
        'submission_id': submission.id,
        'exam_title': exam.title,
        'student_name': submission.student_name,
        'score': submission.score,
        'total_score': submission.total_score,
        'time_taken': submission.time_taken,
        'submitted_at': submission.submitted_at.isoformat(),
        'detailed_results': submission.get_detailed_results()
    }
    
    return jsonify(result)

# 启动应用
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)