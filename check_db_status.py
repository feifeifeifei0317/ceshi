from app import app, db, Question

with app.app_context():
    total_count = Question.query.count()
    marx_count = Question.query.filter_by(subject="马克思主义基本原理").count()
    print(f"总题目数: {total_count}")
    print(f"马克思主义题目数: {marx_count}")
