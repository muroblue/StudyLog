import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
DB = 'studylog.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ページ表示
@app.route('/')
def index():
    return render_template('index.html')

# 一覧取得API
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY date ASC').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

# タスク追加API
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    name = data.get('name')
    date = data.get('date', '')
    if not name:
        return jsonify({'error': 'タスク名は必須です'}), 400
    conn = get_db()
    conn.execute('INSERT INTO tasks (name, date) VALUES (?, ?)', (name, date))
    conn.commit()
    conn.close()
    return jsonify({'message': '追加しました'}), 201

# 完了トグルAPI
@app.route('/api/tasks/<int:task_id>/done', methods=['PATCH'])
def toggle_done(task_id):
    conn = get_db()
    task = conn.execute('SELECT done FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        return jsonify({'error': '見つかりません'}), 404
    new_done = 0 if task['done'] else 1
    conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (new_done, task_id))
    conn.commit()
    conn.close()
    return jsonify({'done': bool(new_done)})

# タスク削除API
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '削除しました'})

if __name__ == '__main__':
    app.run(debug=True)