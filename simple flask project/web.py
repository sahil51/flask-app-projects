from flask import*
import mysql.connector

app = Flask(__name__)

app.secret_key = 'super_key'

conncection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',  
    password = 'sahil7070',
    database= 'db1'
)
cursor = conncection.cursor()
@app.route('/')
def home():
    return render_template('web1.html')

@app.route('/reg1')
def regg():
   return render_template('reg1.html')

@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
     fname = request.form['nme']
     username = request.form['use']
     email = request.form['eml']
     phone = request.form['phn']
     password = request.form['psw']
     cpassword = request.form['cpsw']
     gender = request.form['gender']
     if password != cpassword:
         flash('password and confirm password do not match.')
         return render_template('reg1.html')
     
    cursor.execute('SELECT * FROM tb7 WHERE u_name = %s', (username,))
    acnt = cursor.fetchone()

    if acnt:
            flash('Username already exists. Please choose a different username.')
            return render_template('reg1.html')
    else:
            cursor.execute('INSERT INTO tb7(f_name,u_name,eml,phn,psw,cpsw,gender) values(%s,%s,%s,%s,%s,%s,%s)', (fname, username, email, phone, password, cpassword,gender))
            conncection.commit()
            return render_template('success.html')



@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/donee', methods=['POST'])
def logggin():
    if request.method == 'POST':
        username = request.form['use']
        password = request.form['psw']
        cursor = conncection.cursor()
        cursor.execute('SELECT * FROM tb7 WHERE u_name = %s AND psw = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            
            return render_template('web1.html')
        else:
            flash('invalid user and password')
            return redirect(url_for('login'))


        
@app.route('/admin')
def admin():
   return render_template('admin.html')

db = {
   'host': 'localhost',
   'user': 'root',
   'password': 'sahil7070',
   'database': 'db1',
}

@app.route('/admin',methods = ['POST'])

def loggin():
   
   if request.method == 'POST':
      username = request.form['use']
      password = request.form['psw']
      if (username == 'asus') and password == 'a':
        conncection = mysql.connector.connect(**db)
        cursor = conncection.cursor(dictionary=True)
        cursor.execute('select * from tb7')
        data = cursor.fetchall()
        cursor.close()
        return render_template('table.html',data=data)
      else:
         flash('Invalid username or password')
         return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    conncection=mysql.connector.connect(**db)
    cursor=conncection.cursor(dictionary=True)
    cursor.execute('select * from tb7')
    data = cursor.fetchall()
    cursor.close()
    conncection.close()
    return render_template("table.html",data=data)


@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    conncection = mysql.connector.connect(**db)
    cursor = conncection.cursor(dictionary=True)
    cursor.execute('DELETE FROM tb7 WHERE id = %s',(id,))
    conncection.commit()
    cursor.close()
    return redirect('/dashboard')



@app.route('/update/<int:id>',methods=['POST','GET'])
def up(id):
    conncection = mysql.connector.connect(**db)
    cursor = conncection.cursor(dictionary=True)
    if request.method=='POST':
        fname = request.form.get('nme')
        username = request.form.get('use')
        email = request.form.get('eml')
        phone = request.form.get('phn')
        password = request.form.get('psw')
        cpassword = request.form.get('cpsw')
        gender = request.form.get('gender')

        if password!=cpassword:
            flash('password and confirm password do not match.')
            return render_template('upadate.html')
        
     
        cursor.execute('use db1')
        cursor.execute('''
                UPDATE  tb7  
                SET f_name = %s, u_name = %s, eml = %s, phn = %s, psw = %s, cpsw = %s, gender = %s
                WHERE id =%s
            ''',(fname,username,email,phone,password,cpassword,gender,id))
        conncection.commit()
        cursor.close()
        conncection.close()
        return redirect('/dashboard')
    else:
        cursor.execute('SELECT * FROM tb7 WHERE id = %s',(id,))
        u_d = cursor.fetchone()
        cursor.close()      
        conncection.close()
        return render_template('upadate.html',data=u_d)

@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=='POST':
        fname = request.form.get('nme')
        username = request.form.get('use')   
        email = request.form.get('eml')
        phone = request.form.get('phn')
        password = request.form.get('psw')
        cpassword = request.form.get('cpsw')
        gender = request.form.get('gender')
        if password!=cpassword:
            flash('password and confirm password do not match.')
            return render_template('/add')
        cursor = conncection.cursor(dictionary=True)
        cursor.execute('use db1')
        cursor.execute('''
                       INSERT INTO tb7 (f_name, u_name, eml, phn, psw, cpsw, gender)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                       ''',(fname,username,email,phone,password,cpassword,gender))
        conncection.commit()
        cursor.close()
        conncection.close() 
        return redirect('/dashboard')
    else:
        return render_template('add.html')

if __name__=='__main__':
    app.run(debug=True)

