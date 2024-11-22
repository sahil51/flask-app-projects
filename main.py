from flask import*
from flask_mail import *
import mysql.connector
from random import randint

Connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='sahil7070',
        database='db1'
    )

cursor = Connection.cursor()

app = Flask(__name__)
app.secret_key='super_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']='sahilrajputygamer@gmail.com' #(use your mail )
app.config['MAIL_PASSWORD']='ubfi gdwa cozq xquk'         #(use your mail password genrated by gmail for less secure apps )
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



mail = Mail(app)

otp = randint(0000,9999)
@app.route('/')
def index():
    return render_template('index.html')


##################################################### registration ############################################################
@app.route('/registraion')
def sign_up_page():
    return render_template('registraion.html')

@app.route('/register', methods=['POST'])
def sign_up():
    uname = request.form['username']
    Name = request.form['name']
    email = request.form['email']
    session['email']=email
    phone = request.form['phone']
    gender = request.form['gender']
    password = request.form['password']
    cpassword = request.form['cpassword']
    
    if password != cpassword:
        flash("Passwords do not match. Please try again.")
        return redirect(url_for('sign_up_page'))
    
    cursor.execute("SELECT * FROM tb9 WHERE uname = %s", (uname,))
    ADX = cursor.fetchone()
    
    if ADX:
        flash("Username already taken. Please choose a different Email.")
        return redirect(url_for('sign_up_page'))
    
    cursor.execute("SELECT * FROM tb9 WHERE email = %s", (email,))
    ADc = cursor.fetchone()
    if ADc:
        flash("Email already taken. Please choose a different username.")
        return redirect(url_for('sign_up_page'))
    

    else:
        global otp
        otp = randint(0000,9999)
        msg = Message(sender='sahilrajputygamer@gmail.com',recipients=[email],subject='one time password(otp)',body=f"Hello {uname},\n\nYour one-time password (OTP) is {otp}.\n\nPlease use this OTP to complete your action. It will expire shortly.")
        mail.send(msg)
    cursor.execute('INSERT INTO tb9 (uname, name, email, phn, gender, psw, cpsw) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                   (uname, Name, email, phone, gender, password, cpassword))
    Connection.commit()
    flash("Registration successful! Please verify your email using the OTP sent to your email address.")
    return redirect(url_for('verify_otp'))





##################################################### OTP varified ############################################################
@app.route('/varify')
def verify_otp():
    return render_template('otp.html')

@app.route('/varified',methods=['POST'])
def verify():
    if request.method=='POST':
        otp1=request.form['otp1']
        otp2 =request.form['otp2']
        otp3 =request.form['otp3']
        otp4 =request.form['otp4']
        ottp = otp1 + otp2 + otp3 + otp4
    if otp == int(ottp):
        flash("OTP verified successfully! You can now log in.")
        return redirect(url_for('sign_in_'))
    else:
        flash("The OTP you entered is incorrect. Please try again.")
        return redirect(url_for('verify_otp'))




####################################################### Resend OTP ############################################################
@app.route('/resendotp', methods=['POST'])
def resend_otp():    
        email = session.get('email') 
        if email:
            global otp
            otp = randint(0000,9999)
            msg = Message(sender='sahilrajputygamer@gmail.com', recipients=[email],subject='one time password(otp)',body=f'Hello,\n\n We have received your request to resend the OTP. Your new OTP is: {otp}\n\n Please use this OTP to complete your registration.'   )
            mail.send(msg)
            flash("A new OTP has been sent to your email. Please check your inbox and enter it to complete your registration.")
            return redirect(url_for('verify_otp')) 
        else:
            flash('Email not found. Please register first.')
            return redirect(url_for('sign_up_page'))
    
  


####################################################### User login ############################################################
@app.route('/login')
def sign_in_():
      return render_template("login.html")

@app.route("/success",methods=['POST'])
def sucess():
    if request.method=='POST':
        uname = request.form['uname']
        password=request.form['psw']
        cursor.execute('SELECT * FROM tb9 where uname=%s AND psw=%s',(uname,password,))
        adc = cursor.fetchone()
        if adc:
            session['user_email'] = adc[4]
            flash("Login successful! Welcome back.")
            return render_template('index.html')
        else:
           flash("Invalid username or password. Please try again.")
           return redirect(url_for('sign_in_'))
        

############################################## fogetton password ################################################################
@app.route("/varifiedd")
def frgt_psw():
    return render_template ("email.html")

@app.route("/varifieed",methods=["POST"])
def udtpsw():
    if request.method=='POST':
        email=request.form['email']
        session['email']=email
        global otp
        otp = randint(0000,9999)
        msg = Message(sender='sahilrajputygamer@gmail.com',recipients=[email],subject='one time password(otp)',body=f'Hello,\n\nYou have requested to reset your password. Your one-time OTP for this request is: {otp}\n\nPlease use this OTP to reset your password.')
        mail.send(msg)
        flash('A one-time OTP has been sent to your email address. Please check your inbox and enter the OTP to proceed with changing your password.')
        return render_template("udtpotp.html")

app.route('udtotp')
def udtpotp():
    return render_template('udtpotp.html')

@app.route("/udtpsw",methods=['POST'])
def udt_psw():
    if request.method=='POST':
        otp1=request.form['otp1']
        otp2=request.form['otp2']
        otp3=request.form['otp3']
        otp4=request.form['otp4']
        attp = otp1 + otp2 + otp3 + otp4
        if int(attp)==(otp):
           flash("OTP verified successfully! You can now change your Password.")
           return render_template("udtpsw.html")
        else:
            flash('invalid otp')
            # return redirect(url_for('udt_psw'))
            return render_template("udtpotp.html")
        
@app.route('/updatepassword')
def utd():
    return render_template('udtpsw.html')

@app.route("/update_password", methods=['POST'])
def chnage_psw():
    if request.method == 'POST':
        password = request.form['npsw']
        cmpassword = request.form['ncpsw']
        
       
        if password != cmpassword:
            flash("Passwords do not match! Please try again.")
            return redirect(url_for('utd'))

        email = session.get('email') 
        
       
        if email:
           
            cursor.execute('''
                UPDATE tb9 
                SET psw = %s, cpsw = %s
                WHERE email = %s
            ''', (password, cmpassword, email))
            Connection.commit() 
            
            flash("Your password has been successfully updated. You can now log in with your new password.")
            return redirect(url_for('sign_in_'))
        else:
            flash("Email not found. Please try again.")
            return redirect(url_for('utd'))





##################################################### Admin autanication ######################################################
@app.route('/admin')
def ad_min():
    return render_template('admin.html')

@app.route('/done',methods=['POST'])
def ad__min():    
    if request.method=='POST':
        name=request.form['uname']
        password=request.form['psw']
        if (name == 'asus') and (password == "asus"):
            session["name"] = name
            cursor = Connection.cursor(dictionary=True)
            cursor.execute('select * from tb9')
            data = cursor.fetchall()
            cursor.close()
            flash("Admin login successful. Welcome to the Admin Dashboard.")
            return render_template('table.html', data = data,name=name)
       
        else:
            flash("Invalid admin username or password. Please try again.")
            return redirect(url_for('ad_min'))

@app.route("/Logout")
def lo_out():
        session.pop('name',None)
        flash("logout successfull")
        return render_template("login.html")


db = {'host':'localhost','user':'root','password':'sahil7070','database':'db1'}


##################################################### Admin Dashboard ######################################################
@app.route('/dashboard')
def dashboard():
    conncection=mysql.connector.connect(**db)
    cursor=conncection.cursor(dictionary=True)
    cursor.execute('select * from tb9')
    data = cursor.fetchall()
    cursor.close()
    conncection.close()
    return render_template("table.html",data=data)

  


##################################################### Admin View ######################################################
@app.route('/view/<int:id>', methods=['GET'])
def view_user(id):
    
    cursor.execute('SELECT * FROM tb9 WHERE id=%s', (id,))
    user = cursor.fetchone()

  
    if user:
        return render_template(
            'view.html', 
            id=user[0],
            uname=user[1],
            name=user[2],
            email=user[3],
            phn=user[4],
            gender=user[5],
            psw=user[6],
            cpsw=user[7]
        )



##################################################### Admin Delete ######################################################
@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    conncection = mysql.connector.connect(**db)
    cursor = conncection.cursor(dictionary=True)
    cursor.execute('DELETE FROM tb9 WHERE id = %s',(id,))
    conncection.commit()
    cursor.close()
    flash('User deleted successfully.', 'success') 
    return redirect('/dashboard')



##################################################### Admin Update ######################################################
@app.route('/modify/<int:id>',methods=['POST','GET'])
def up(id):
    conncection = mysql.connector.connect(**db)
    cursor = conncection.cursor(dictionary=True)
    if request.method=='POST':
        uname = request.form['username']
        Name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['password']
        cpassword = request.form['cpassword']

        if password!=cpassword:
            flash('Password and confirm password do not match.', 'error')
            return render_template('update.html')
        
        
        if not all ([uname,Name,email,phone,gender,password,cpassword]):
             flash('All fields are required.', 'error')
        cursor.execute('use db1')
        cursor.execute('''
                UPDATE  tb9
                SET  uname = %s, name = %s, email = %s, phn = %s, gender = %s, psw = %s, cpsw = %s
                WHERE id =%s
            ''',(uname,Name,email,phone,gender,password,cpassword,id))
        conncection.commit()
        flash('User details updated successfully.', 'success') 
        cursor.close()
        conncection.close()
        return redirect('/dashboard')
    else:
        cursor.execute('SELECT * FROM tb9 WHERE id = %s',(id,))
        data = cursor.fetchone()
        cursor.close()      
        conncection.close()
        return render_template('update.html',data=data)
    


##################################################### Admin Add ######################################################
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        uname = request.form['username']
        Name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['password']
        cpassword = request.form['cpassword']
        

        if not all([uname, Name, email, phone,gender, password, cpassword]):
            flash('All fields are required.', 'error')
            return render_template('add.html')

        if password != cpassword:
            flash('Password and confirm password do not match.', 'error')
            return render_template('add.html')

        cursor = Connection.cursor()
        cursor.execute('''
            INSERT INTO tb9 (uname, name, email, phn,gender, psw, cpsw)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (uname,Name, email, phone,gender, password, cpassword))
        Connection.commit()
        cursor.close()
        flash('User added successfully.', 'success')
        return redirect('/dashboard')
    else:
        return render_template('add.html')

if __name__=='__main__':
    app.run(debug=True)



  
