from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

