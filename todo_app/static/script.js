let token = localStorage.getItem('token');

function showAddPopup() {
  document.getElementById('addModal').style.display = 'block';
}

function hideAddPopup() {
  document.getElementById('addModal').style.display = 'none';
}

function loadTasks() {
  fetch('/tasks', {
    headers: { 'Authorization': 'Bearer ' + token }
  })
  .then(res => res.json())
  .then(data => {
    let container = document.getElementById('taskContainer');
    container.innerHTML = '';
    data.forEach(task => {
      container.innerHTML += `
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <h5>${task.title}</h5>
              <p>${task.content}</p>
            </div>
          </div>
        </div>`;
    });
  });
}

function addTask() {
  const title = document.getElementById('title').value;
  const content = document.getElementById('content').value;

  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({ title, content })
  })
  .then(res => {
    hideAddPopup();
    loadTasks();
  });
}

window.onload = function () {
  if (token) {
    loadTasks();
    document.getElementById('auth-buttons').innerHTML = `<button class="btn btn-secondary">Profile</button>`;
  }
};
