import mysql.connector
import yaml
import os

db = yaml.load(open('db.yaml'))
host = db['mysql_host']
user = db['mysql_user']
password = db['mysql_password']
database = db['mysql_db']

con = mysql.connector.connect(
  host = host,
  user = user,
  password = password,
  database = database
)

cur = con.cursor()
cur.execute("SELECT * FROM users")
with open("database.txt", "w", newline='') as file:
    for (name, email) in cur:
        file.write(f"{name}-{email}\n")

os.system("git add -A")
os.system("git commit -m 'pushing to heroku'") 
os.system("git push")
