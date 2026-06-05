import sqlite3

def init_db():
    conn = sqlite3.connect('studylog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            date  TEXT,
            done  INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("DB初期化完了")

if __name__ == '__main__':
    init_db()