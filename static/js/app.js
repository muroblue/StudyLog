// タスク一覧を取得して描画
async function loadTasks() {
  const res = await fetch('/api/tasks');
  const tasks = await res.json();
  const list = document.getElementById('task-list');
  const emptyMsg = document.getElementById('empty-msg');

  list.innerHTML = '';

  if (tasks.length === 0) {
    emptyMsg.style.display = 'block';
    return;
  }

  emptyMsg.style.display = 'none';

  tasks.forEach(task => {
    const li = document.createElement('li');
    li.className = 'task-item' + (task.done ? ' done' : '');
    li.innerHTML = `
      <span class="task-name">${task.name}</span>
      <span class="task-date">${task.date || '日付なし'}</span>
      <button class="done-btn" onclick="toggleDone(${task.id})">
        ${task.done ? '戻す' : '完了'}
      </button>
      <button class="delete-btn" onclick="deleteTask(${task.id})">削除</button>
    `;
    list.appendChild(li);
  });
}

// タスク追加
document.getElementById('add-btn').addEventListener('click', async () => {
  const name = document.getElementById('task-name').value.trim();
  const date = document.getElementById('task-date').value;
  const errorMsg = document.getElementById('error-msg');

  if (!name) {
    errorMsg.textContent = 'タスク名を入力してください';
    return;
  }
  errorMsg.textContent = '';

  await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, date })
  });

  document.getElementById('task-name').value = '';
  document.getElementById('task-date').value = '';
  loadTasks();
});

// 完了トグル
async function toggleDone(id) {
  await fetch(`/api/tasks/${id}/done`, { method: 'PATCH' });
  loadTasks();
}

// タスク削除
async function deleteTask(id) {
  await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
  loadTasks();
}

// 初回読み込み
loadTasks();