from flask import Flask , render_template , request , redirect , url_for
import sqlite3

app = Flask(__name__)

try:
#initialize Database

def initializeDatabase():
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS namelist
                 (id INTEGER PRIMARY KEY, name TEXT, paidstatus INTEGER)''')
    connector.commit()
    connector.close()
    
    initializeDatabase()
    
    
#add data to database
@app.route('/add',methods=['POST'])
def add_item():
    name = request.form['name']
    paidstatus = request.form['paidstatus']
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    c.execute("INSERT INTO items (name , paidstatus ) VALUES (? , ? )" ,(name , paidstatus))
    connector.commit()
    connector.close()
    return redirect(url_for('index.html'))

#search function
@app.route('/search',methods=['POST'])
def search():
    query = request.args.get('query')
    connector = sqlite3.connect('data.db')
    
    
except:
    print("something Went Wrong")