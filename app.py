from flask import Flask ,jsonify,request
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS
import os
import bcrypt
from functools import wraps
from datetime import datetime,timedelta
import jwt

load_dotenv()


app=Flask(__name__)
CORS(app)
app.config['SECRET_KEY']=os.getenv("SECRET_KEY",'MY_SECRET_KEY')

def get_connection():
    conn=psycopg2.connect(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )
    return conn

def initialize_db():
    conn=get_connection()
    cur=conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY,
                             username TEXT UNIQUE NOT NULL,
                             password TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXIST tasks
                    (id INTEGER PRIMARY KEY,
                     task TEXT NOT NULL,
                     done BOOLEAN DEFAULT FALSE
                     user_id INTEGER REFERENCES users(id) ON DELETE CASCADE)''')
    conn.commit()
    cur.close()
    conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        
        if 'Authorization' in request.headers:
            token=request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message':"Token is missing"}),401
        
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user,*args,**kwargs)
    return decorated

@app.route('/api/signup',methods=['POST'])
def signup():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    
    if not username or not password:
        return jsonify({'message':"username and password are required"}),400
    
    conn=get_connection()
    cur=conn.cursor()
    
    hashed_pw=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    
    try:
        cur.execute("INSERT INTO users(username,password) VALUES (%s%s)",(username,hashed_pw))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'message':'Username already exists'}),400
    cur.close()
    conn.close()
    return jsonify({'message':'User registered successfully'}),201

@app.route('/api/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    
    conn=get_connection()
    cur=conn.cursor
    cur.execute('SELECT password FROM users WHERE username=%s',(username,))
    user=cur.fetchone()
    cur.close()
    conn.close()
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return jsonify({'message': 'Invalid username or password!'}), 401

    token = jwt.encode(
        {'username': username, 'exp': datetime.utcnow() + timedelta(hours=2)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({'token': token})

@app.route('/api/tasks',methods=['GET'])
@token_required
def get_task(current_user):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT id FROM users WHERE username =%s",(current_user,))
    user_id=cur.fetchone()[0]
    
    cur.execute("SELECT * from tasks WHERE user_id=%s ORDER BY id ASC",(user_id))
    tasks=cur.fetchall()
    cur.close()
    conn.close()
    
    result=[{"id":t[0],"task":t[1],"done":t[2]}
            for t in tasks
            ]
    return jsonify(result)

@app.route('/api/tasks',methods=['POST'])
def add_task():
    data=request.get_json()
    task=data.get("task")
    
    conn=get_connection()
    cur=conn.cursor()
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
    initialize_db()
    app.run(debug=True)
    