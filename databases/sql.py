import mysql.connector


mydb = mysql.connector.connect(
    host="127.0.0.1:3306",
    user="root",
    password="123"
)

print(mydb)