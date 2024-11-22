# from flask import*
# import mysql.connector 
# app = Flask(__name__)
# Connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='sahil7070',
#         database='db1'
#     )

# @app.route('/')
# def db(uname, Name,email,phone,gender,password,cpassword):
   
#     cursor = Connection.cursor()
#     # cursor.execute("CREATE TABLE  tb9(id INT  PRIMARY KEY AUTO_INCREMENT,uname VARCHAR(90),name VARCHAR(90),email VARCHAR(190),phn VARCHAR(59),gender ENUM('M','F'),psw VARCHAR(80),cpsw VARCHAR(90))")
#     cursor.execute('insert into tb9(uname,name,email,phn,gender,psw,cpsw)values(%s,%s,%s,%s,%s,%s,%s)',uname, Name,email,phone,gender,password,cpassword)
    
#     Connection.commit()
#     return 'done'

# if __name__=='__main__':
#     app.run(debug=True)



from flask import*
import mysql.connector 
app = Flask(__name__)
Connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='sahil7070',
        database='db1'
    )

@app.route('/')
def db():
   
    cursor = Connection.cursor()
    cursor.execute("CREATE TABLE  tb10(id INT  PRIMARY KEY AUTO_INCREMENT,uname VARCHAR(90),name VARCHAR(90),email VARCHAR(190),phn VARCHAR(59),gender ENUM('M','F'),psw VARCHAR(80),cpsw VARCHAR(90))")
    # cursor.execute('insert into tb9(uname,name,email,phn,gender,psw,cpsw)values(%s,%s,%s,%s,%s,%s,%s)',uname, Name,email,phone,gender,password,cpassword)
    
    Connection.commit()
    return 'done'

if __name__=='__main__':
    app.run(debug=True)