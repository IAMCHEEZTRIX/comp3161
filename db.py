import mysql.connector


def get_db_connection():
    db = mysql.connector.connect(host="localhost", user="COMP3161", password="password", database="comp3161project")
    return db