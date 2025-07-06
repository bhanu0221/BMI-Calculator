from flask import Flask,render_template,request,redirect,Response,url_for,session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "private key"

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='8865876746Bhanushahi',
        database='mini_project'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",
                           (name,email,password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        
        except mysql.connector.IntegrityError:
            return "Email allready exists"
        except Error as e:
            return f"database error:{e}"
        
    return render_template('register.html')

@app.route('/login', methods =["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                return "Invalid email or password."
            
        except Error as e:
            return f"database error:{e}"
        
    return render_template('login.html')   


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', name=session['user_name'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/bmi', methods=['GET', 'POST'])
def bmi_calculator():
    bmi_result = None
    category = None

    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height']) / 100  # Convert cm to meters

            bmi = round(weight / (height ** 2), 2)

            # Determine BMI category
            if bmi < 18.5:
                category = 'Underweight'
            elif 18.5 <= bmi < 24.9:
                category = 'Normal weight'
            elif 25 <= bmi < 29.9:
                category = 'Overweight'
            else:
                category = 'Obese'

            bmi_result = bmi
        except:
            bmi_result = 'Invalid input'

    return render_template('bmi.html', bmi=bmi_result, category=category)



if __name__ == '__main__':
    app.run(debug=True)

