from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 仮のタスクデータ（後でDBに置き換える）
    tasks = [
        {'id': 1, 'name': '線形代数のレポート', 'date': '2025-06-10', 'done': False},
        {'id': 2, 'name': 'アルゴリズムの課題',  'date': '2025-06-05', 'done': True},
    ]
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)