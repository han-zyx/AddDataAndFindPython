from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Initialize Database
def initializeDatabase():
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS namelist
                 (id INTEGER PRIMARY KEY, name TEXT, paidstatus TEXT, ticket TEXT)''')  # Added 'ticket' column
    connector.commit()
    connector.close()


initializeDatabase()


# Add data to database
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    paidstatus = request.form['paidstatus']
    ticket = request.form['ticket']  # Get ticket value from form
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    c.execute("INSERT INTO namelist (name, paidstatus, ticket) VALUES (?, ?, ?)", (name, paidstatus, ticket))
    connector.commit()
    connector.close()
    return redirect(url_for('index'))

#update ticket status
@app.route('/update_ticket/<int:item_id>', methods=['POST'])
def update_ticket(item_id):
    new_ticket = request.form['new_ticket']
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    c.execute("UPDATE namelist SET ticket = ? WHERE id = ?", (new_ticket, item_id))
    connector.commit()
    connector.close()
    return redirect(url_for('index'))


# Delete function
@app.route('/delete_selected_items', methods=['POST'])
def delete_selected_items():
    selected_items = request.form.getlist('selected_items')
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    
    for item_id in selected_items:
        c.execute("DELETE FROM namelist WHERE id=?", (item_id,))
        c.execute("SELECT * FROM namelist")
    connector.commit()
    connector.close()
    return redirect(url_for('index'))


# Search function
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    if query:
        c.execute("SELECT * FROM namelist WHERE name LIKE ? OR paidstatus LIKE ? OR ticket LIKE ?",
                  ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        c.execute("SELECT * FROM namelist")
    namelist = c.fetchall()
    connector.close()
    return render_template('index.html', namelist=namelist)


# Homepage route
@app.route('/')
def index():
    connector = sqlite3.connect('data.db')
    c = connector.cursor()
    # c.execute("SELECT * FROM namelist")
    namelist = c.fetchall()
    connector.close()
    return render_template('index.html', namelist=namelist)



if __name__ == '__main__':
    app.run(debug=True)

