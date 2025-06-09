from flask import Flask, request, jsonify
import psycopg2
import time

app = Flask(__name__)

# Ждём доступности БД
for i in range(10):
    try:
        conn = psycopg2.connect(
            host="db",
            database="docker",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        break
    except Exception as e:
        print("⏳ Ждём PostgreSQL...")
        time.sleep(1)
else:
    print("❌ Не удалось подключиться к БД.")
    exit(1)

# Создание таблицы, если не существует
cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL
    )
""")
conn.commit()


@app.route('/')
def index():
    return "12112232132211🔥 Обновлено через self-hosted CI/CD!"

@app.route('/data', methods=['GET'])
def get_data():
    cur.execute("SELECT * FROM messages")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Поле \"message\" обязательно'}), 400

    message = data['message']
    cur.execute("INSERT INTO messages (text) VALUES (%s) RETURNING id", (message,))
    new_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({'status': 'ok', 'id': new_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
