# todo_app/
# ├── frontend/
# │   ├── index.html
# │   └── style.css
# └── backend/
#     └── app.py

# pip install flask
# cd backend
# python app.py
# http://127.0.0.1:5000

from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

# Simple in-memory storage (will reset when server restarts)
###global tasks ???
tasks = []

# Load tasks from JSON file if it exists
if os.path.exists('tasks.json'):
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)

# Настройка папки для статических файлов
app.config['STATIC_FOLDER'] = os.path.abspath('../frontend')

@app.route('/')
def index():
    return send_from_directory(app.config['STATIC_FOLDER'], 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.config['STATIC_FOLDER'], path)


@app.route('/api/tasks')
def get_tasks():
    return jsonify(tasks)


@app.route('/api/add-task', methods=['POST'])
def add_task():
    task_text = request.json.get('text')
    if not task_text:
        return jsonify({'error': 'Task text is required'}), 400

    task_id = len(tasks) + 1
    new_task = {'id': task_id, 'text': task_text}
    tasks.append(new_task)

    # Save to JSON file
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

    return jsonify(new_task), 201


@app.route('/api/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]

    # Update JSON file
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

    return jsonify({}), 204

@app.errorhandler(404)
def page_not_found(e):
    return 'Страница не найдена', 404

@app.errorhandler(500)
def internal_server_error(e):
    return 'Внутренняя ошибка сервера', 500


if __name__ == '__main__':
    app.run(debug=True)



###Создайте файл requirements.txt
###pip freeze > requirements.txt

#Установите CLI для Render
# python -m urllib.request https://render.com/install.py

