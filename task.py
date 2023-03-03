from flask_login import LoginManager, login_user, login_required, logout_user
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, SearchField, SelectField, IntegerField, SelectFieldBase, DateTimeField, SelectMultipleField, StringField
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect
import data.db_session as session
from data.users import User
from data.jobs import Jobs
from wtforms.validators import DataRequired
import datetime



app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

account = ''


def adding_for_test():
    
    user = User()
    user.surname = "Test"
    user.name = "Test"
    user.age = 21
    user.position = "test"
    user.speciality = "test"
    user.address = "module_1"
    user.email = "test@test.org"
    user.password_hash = "test"
    user.set_password("test")

    db_session.add(user)
    
    db_session.commit()


class JobForm(FlaskForm):
    id = IntegerField('Team-leader-id', validators=[DataRequired()])
    title = StringField('Title of job', validators=[DataRequired()])   
    work_size = IntegerField('Work size (in hours)', validators=[DataRequired()])
    collaborators = StringField("collaborators' ID using ,", validators=[DataRequired()])
    start_date = DateTimeField('Start date', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime(year=2023, month=1, day=1, hour=1, minute=0, second=0))
    end_date = DateTimeField('End date', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime(year=2030, month=1, day=1, hour=1, minute=0, second=0))
    done = BooleanField('Is finished?')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])

    age = IntegerField('Age')
    position = StringField('Position')
    speciality = StringField('Speciality')
    address = StringField('Address')
    
    submit = SubmitField('Register')


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


@app.route("/start")
def start():
    global account
    return render_template('base.html', account=account)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global account
    form = LoginForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            account = f'{user.name} {user.surname}'
            login_user(user, remember=form.remember_me.data)
            return redirect("/works")
        
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    
    return render_template('login.html', title='Авторизация', form=form, account='')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global account
    
    account = ''
    form = RegisterForm()
    
    
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registretion.html', title='Register form', form=form, message="Пароли не совпадают, перевведите.")
        
        if db_session.query(User).filter(User.email == form.email.data).first():
            return render_template('registretion.html', title='Register form', form=form, message="Почта уже используется")
        
        #print(form.name.data, form.email.data, form.surname.data, form.age.data, form.position.data, form.address.data, form.speciality.data, form.password.data)
        
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            address=form.address.data,
            speciality=form.speciality.data
        )
        
        user.set_password(form.password.data)
        
        db_session.add(user)
        db_session.commit()
        
        return redirect('/login')
    
    return render_template('registretion.html', title='Register form', form=form, account='')


@app.route('/logout')
@login_required
def logout():
    global account
    
    account = ''
    
    logout_user()
    return redirect("/")


@app.route('/works')
@login_required
def table():
    res = db_session.query(Jobs).all()
    data = []

    for job in res:

        time = f'{round((job.end_date - job.start_date).total_seconds() / 3600)} hours'
        user = db_session.query(User).filter(User.id == job.team_leader).first()
        team_leader = user.name + ' ' + user.surname

        data.append([job.job, team_leader, time, job.collaborators, job.is_finished])

    return render_template('works.html', jobs=data, account=account)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    global account
    form = JobForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter(User.id == form.id.data).first()
        if user:
            jobs = Jobs()
            jobs.team_leader = form.id.data
            jobs.job = form.title.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.done.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            
            db_session.add(jobs)
            db_session.commit()

            return redirect("/works")
        
        return render_template('job_add.html', message="WRONG Email Adress", form=form, account=account)
        
    return render_template('job_add.html', title='Adding JOB', form=form, account=account)


if __name__ == '__main__':
    session.global_init("db/blogs.db")
    db_session = session.create_session()
    
    app.run(port=8080, host='127.0.0.1')
    
    adding_for_test() #для того чтобы войти в систему