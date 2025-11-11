from flask import Flask ,jsonify,request
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app=Flask(__name__)
CORS(app)


def get_connection():
    conn=psycopg2.connect(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )
    return conn

@app.route('/api/tasks',methods=['GET'])
def get_task():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("Select * from tasks Order by id ASC")
    tasks=cur.fetchall()
    cur.close()
    conn.close()
    
    result=[{"id":t[0],"task":t[1],"done":t[2]}
            for t in tasks
            ]
    
    return jsonify(result)
print("this is done")

@app.route('/api/tasks',methods=['POST'])
def add_task():
    data=request.get_json()
    task=data.get("task")
    
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("Create table if not exists tasks(id SERIAL PRIMARY KEY,task TEXT NOT NULL,done BOOLEAN DEFAULT FALSE)")
    cur.execute("INSERT INTO tasks (task) VALUES (%s)",(task,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message":"Task added"}),201

@app.route('/api/tasks/<int:task_id>',methods=['PUT'])
def complete_task(task_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("UPDATE tasks SET done=TRUE WHERE id =%s",(task_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message":"Task completed"}) 

@app.route('/api/tasks/<int:task_id>',methods=['DELETE'])
def delete_data(task_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s",(task_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message":"Task deleted"})

if __name__=="__main__":
    app.run(debug=True)
    