import csv

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_login import login_required, LoginManager, UserMixin
from database import Database

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'AlparslanTurkesScienceAndTechnologyUniversity'

#login_manager = LoginManager() //For login requiered
#login_manager.init_app(app) //For login requiered

obs_students_database = Database('obs', 'students_credentials')
obs_academicians_database = Database('obs', 'academicians_credentials')
obs_students_grades = Database('obs', 'students_grades')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/acd_login', methods=['GET', 'POST'])
def acd_login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        account = obs_academicians_database.acd_login(mail, password)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return redirect(url_for('acd_dashboard'))
        message = 'Incorrect username/password!'
        return render_template('acd_login.html', message=message)

    return render_template('acd_login.html')


@app.route('/std_login', methods=['GET', 'POST'])
def std_login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        account = obs_students_database.std_login(mail, password)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['mail'] = account[1]
            return redirect(url_for('std_dashboard'))

        message = 'Incorrect username/password!'
        return render_template('std_login.html', message=message)
    return render_template('std_login.html')


@app.route('/std_dashboard')
def std_dashboard():
    return render_template('std_dashboard.html')


@app.route('/acd_dashboard')
def acd_dashboard():
    return render_template('acd_dashboard.html')

@app.route('/std_grades')
def std_grades():
    id = session['id']
    grades = obs_students_grades.id_to_grades(id)[1:]
    return render_template('std_grades.html', grades=grades)


@app.route('/acd_students')
def acd_students():
    mails = obs_students_database.fetch_all_students()
    return render_template('acd_students.html', mails=mails)


@app.route('/acd_grades', defaults={'id': 0}, methods=['GET', 'POST'])
@app.route('/acd_grades/<int:id>', methods=["GET", "POST"])
def acd_grades(id):
    if request.method == 'POST':
        alg = int(request.form['alg'])
        spd = int(request.form['spd'])
        ld = int(request.form['ld'])
        ds = int(request.form['ds'])
        os = int(request.form['os'])
        clc = int(request.form['clc'])
        obs_students_grades.update_grade(id, alg, spd, ld, ds, os, clc)
        return redirect(url_for('acd_grades', id=id))
    mails = obs_students_database.fetch_all_students()
    std_grades = obs_students_database.id_to_grades(id)
    print("Test Line")
    print(std_grades)
    return render_template('acd_grades.html', mails=mails, std_grades=std_grades)


@app.route('/std_lessons')
def std_lessons():
    return render_template('std_lessons.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/academic_calendar')
def academic_calendar():
    return render_template('academic_calendar.html')

@app.route('/food_list')
def food_list():
    return render_template('food_list.html')

@app.route('/numbers')
def numbers():
    return render_template('numbers.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('mail', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
