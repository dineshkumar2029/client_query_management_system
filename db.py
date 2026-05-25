import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="client_query_system"
)

cursor = connection.cursor()