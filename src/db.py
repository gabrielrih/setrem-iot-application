import mysql.connector
import requests
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


''' Busca data e hora online '''
def busca_data():
    url = "http://worldtimeapi.org/api/timezone/America/Sao_Paulo"
    payload = ""
    response = requests.request("GET", url, data=payload)
    dtexec = response.json()['unixtime']
    return dtexec

''' Salva dados na base de dados (MySQL)'''
def save_data(temperature, humidity):
    mydb = mysql.connector.connect(
                host="mysql",
                user="root",
                port="3306",
                password="1234",
                database="dbiot"
                )
    mycursor = mydb.cursor()
    sql = "INSERT INTO TORRE (temp,umid,dtexec) VALUES (%s, %s, %s)"
    val = (temperature,humidity,busca_data())
    mycursor.execute(sql, val)
    mydb.commit()
