from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)
database = './db.sqlite'

@app.route('/')
def index():

    # making connection with database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # fetching existing data from database
    c.execute("SELECT * FROM student")
    rs = c.fetchall()

    return render_template('index.html', rs=rs)

# ------ ADDING NEW STUDENT DATA TO DATABASE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # saving data from form into variables
        studname = request.form['studname']
        studemail = request.form['studemail']
        studphone = request.form['studphone']
        post = request.form['post']
        department = request.form['department']

        # making connection with database
        conn = sqlite3.connect(database)
        c = conn.cursor()

        # inserting into database
        c.execute("""INSERT into student (studname, studemail, studphone, post, department) VALUES (?, ?, ?, ?, ?)""",
                    (studname, studemail, studphone, post, department))
        
        # committing the changes into the database
        conn.commit()

        # closing the database connection
        conn.close()

        return redirect(url_for('index'))

# ------ UPDATING STUDENT DATA
@app.route('/update<int:id>', methods=['GET', 'POST'])
def update(id):
    # making connection to database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # fetching the selected student data
    c.execute("SELECT * FROM student WHERE id = '"+str(id)+"'")
    rs = c.fetchone()

    if request.method == 'POST':
        # saving new data from form into variables
        studname = request.form['studname']
        studemail = request.form['studemail']
        studphone = request.form['studphone']
        post = request.form['post']
        department = request.form['department']

        # updating data in database
        c.execute("""UPDATE student SET (studname, studemail, studphone, post, department) = (?, ?, ?, ?, ?) WHERE id = ?""",
                    (studname, studemail, studphone, post, department, str(id)))
        
        # committing the changes into the database
        conn.commit()

        # closing the database connection
        conn.close()

        return redirect(url_for('index'))

    return render_template('update.html', rs=rs)

# ------ DELETING STUDENT DATA
@app.route('/delete<int:id>')
def delete(id):
    # making connection with database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # deleting the data
    c.execute("DELETE FROM student WHERE id = '"+str(id)+"'")

    # committing the changes
    conn.commit()

    # closing the connection
    conn.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)