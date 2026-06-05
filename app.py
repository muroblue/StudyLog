import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = 'studylog.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # 辞書形式でアクセスできるようにする
    return conn

# 一覧表示
@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY date ASC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# タスク追加
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    date = request.form['date']
    conn = get_db()
    conn.execute('INSERT INTO tasks (name, date) VALUES (?, ?)', (name, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 完了トグル
@app.route('/done/<int:task_id>')
def done(task_id):
    conn = get_db()
    task = conn.execute('SELECT done FROM tasks WHERE id = ?', (task_id,)).fetchone()
    new_done = 0 if task['done'] else 1
    conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (new_done, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# タスク削除
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)