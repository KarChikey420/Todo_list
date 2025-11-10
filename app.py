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
