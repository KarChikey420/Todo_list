from flask import Flask ,render_template,redirect,request
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

def get_connection():
    conn=get_connection(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('postgres'),
        password=os.getenv('password')
    )

@app.route('/')
def index():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("Create table if not exists task(id SERIAL PRIMARY KEY,task TEXT NOT NULL,done BOOLEAN DEFAULT FALSE)")
    cur.execute("Select * from task Order by id ASC")
    tasks=cur.fetchall()
    cur.close()
    conn.close()
    return render_template()