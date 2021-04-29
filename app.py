# Make sure to install the following tools
# sudo apt-get install python-dev default-libmysqlclient-dev libssl-dev
# pip install --user flask-mysqldb
# Login to MySQL with root
# Create a new user: CREATE USER 'user'@'%' IDENTIFIED BY 'YOUR_PASSWORD';
# Grant Priviledges: GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)

#Conditionally configure database
print(os.environ.get("RUNNING_ON_HEROKU"))
db = ""
if os.environ.get("RUNNING_ON_HEROKU") == "True":
    db = yaml.load(open('cleardb.yaml'))
    print(db)
else:
    db = yaml.load(open('db.yaml'))
    print(db)
    
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("made it to index!")
    if request.method == 'POST':
        # Fetch form data
        print("detected post method!")
        userDetails = request.form
        print(userDetails)
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run()