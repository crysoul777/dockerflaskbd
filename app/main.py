from flask import Flask, jsonify
import psycopg2
import time

app = Flask(__name__)

# подождать, пока база запустится
time.sleep(5)

def get_connection():
    return psycopg2.connect(
        dbname="testdb",
        user="user",
        password="pass",
        host="db"
    )

@app.route("/")
def index():
    return "👋 Flask работает в Docker!"

@app.route("/data")
def data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO test (name) VALUES (%s)", ("Запись из Flask",))
    conn.commit()

    cur.execute("SELECT * FROM test;")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
